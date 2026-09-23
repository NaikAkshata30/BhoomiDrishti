"""Public HTTP only: TLS verification, host allowlist, throttling, no login/CAPTCHA."""
import urllib.request, urllib.error
from urllib.parse import urlparse
import threading, time, subprocess, tempfile, json
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit, urljoin

HOSTS={'upeida.up.gov.in','morth.nic.in','morth.gov.in','nhai.gov.in','bhoomirashi.gov.in','bhoomirashi.nic.in','delhimetrorail.com','backend.delhimetrorail.com','corporate.mmrcl.com','corporate-old.mmrcl.com','mmrcl.com','chennaimetrorail.org','wcag.chennaimetrorail.org','nhidcl.com','msrdc.in','dfccil.com','pib.gov.in','static.pib.gov.in','sansad.in','environmentclearance.nic.in','forestsclearance.nic.in','parivesh.nic.in','imdpune.gov.in','mausam.imd.gov.in','dsp.imdpune.gov.in','ganderbal.nic.in','dausa.rajasthan.gov.in','rudraprayag.gov.in','meerut.nic.in','prayagraj.nic.in','sambhal.nic.in','hapur.nic.in','ladakh.gov.in','sci.gov.in','api.sci.gov.in','webapi.sci.gov.in','bhuvan.nrsc.gov.in','ndem.nrsc.gov.in','data.gov.in','eprocure.gov.in','services.ecourts.gov.in','etender.up.nic.in','mahatenders.gov.in','cdn.s3waas.gov.in'}
HOSTS.update({'jica.go.jp','libportal.jica.go.jp','openjicareport.jica.go.jp','dmrelief.rajasthan.gov.in'})
locks={}; gate=threading.Lock(); blocked=set()
def host(url): return (urlparse(url).hostname or '').lower().removeprefix('www.')
def check(url):
    if urlparse(url).scheme not in ('http','https') or host(url) not in HOSTS:
        raise ValueError('unapproved_public_host: '+url)
def windows_verified_fetch(url,max_bytes,depth=0):
    """Schannel uses Windows certificate-chain building; never disables TLS checks."""
    check(url)
    if depth>5: raise RuntimeError('too_many_redirects')
    with tempfile.TemporaryDirectory(prefix='bhoomidrishti_') as temp:
        bodypath=Path(temp)/'body'; headerspath=Path(temp)/'headers'
        result=subprocess.run(['curl.exe','--silent','--show-error','--max-time','60','--max-filesize',str(max_bytes),'--proto','=https,http','--user-agent','BhoomiDrishti-Research/1.0 (public-document-collection)','--dump-header',str(headerspath),'--output',str(bodypath),'--write-out','%{json}',url],capture_output=True,text=True,timeout=70)
        if result.returncode: raise RuntimeError('verified_windows_http_error: '+result.stderr.strip()[:500])
        info=json.loads(result.stdout)
        headers={}
        for line in headerspath.read_text(encoding='latin-1').splitlines():
            if ':' in line:
                k,v=line.split(':',1); headers[k.lower()]=v.strip()
        status=info['http_code']
        if status in (301,302,303,307,308): return windows_verified_fetch(urljoin(url,headers.get('location','')),max_bytes,depth+1)
        if status>=400:
            if status in (401,403,429): blocked.add(host(url))
            raise RuntimeError('HTTP '+str(status))
        body=bodypath.read_bytes()
        if len(body)>max_bytes: raise RuntimeError('size_limit_100MB_manual_download_required')
        ctype=headers.get('content-type','')
        if 'html' in ctype:
            text=body[:250000].decode('utf-8','replace').lower()
            if any(s in text for s in ('verify you are human','checking your browser','request rejected','access denied','cf-chl-','incapsula incident id')):
                blocked.add(host(url)); raise RuntimeError('access_challenge_no_bypass')
        return body,dict(final_url=url,http_status=status,content_type=ctype,last_modified=headers.get('last-modified'),etag=headers.get('etag'),transport='Windows_Schannel_TLS_verified')
class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        check(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)
def fetch(url,max_bytes=100*1024*1024):
    parts=urlsplit(url); url=urlunsplit((parts.scheme,parts.netloc,quote(parts.path,safe='/%:@'),quote(parts.query,safe='=&%/:?+'),parts.fragment))
    check(url); domain=host(url)
    with gate: lock=locks.setdefault(domain,threading.Lock())
    with lock:
        if domain in blocked: raise RuntimeError('host_paused_after_access_restriction')
        time.sleep(0.75)
        req=urllib.request.Request(url,headers={'User-Agent':'BhoomiDrishti-Research/1.0 (public-document-collection)','Accept':'*/*'})
        try:
            with urllib.request.build_opener(Redirects()).open(req,timeout=40) as r:
                chunks=[]; size=0
                while True:
                    chunk=r.read(1024*1024)
                    if not chunk: break
                    size+=len(chunk)
                    if size>max_bytes: raise RuntimeError('size_limit_100MB_manual_download_required')
                    chunks.append(chunk)
                body=b''.join(chunks)
                content_type=r.headers.get('Content-Type','')
                if 'html' in content_type or body.lstrip().lower().startswith(b'<!doctype html'):
                    preview=body[:250000].decode('utf-8','replace').lower()
                    challenge=('verify you are human','checking your browser','request rejected','access denied','captcha validation','cf-chl-','please enable cookies','incapsula incident id')
                    if any(s in preview for s in challenge):
                        blocked.add(domain); raise RuntimeError('access_challenge_no_bypass')
                return body,dict(final_url=r.url,http_status=r.status,content_type=content_type,last_modified=r.headers.get('Last-Modified'),etag=r.headers.get('ETag'))
        except urllib.error.HTTPError as e:
            if e.code in (401,403,429): blocked.add(domain)
            raise
        except urllib.error.URLError as e:
            if 'CERTIFICATE_VERIFY_FAILED' in str(e): return windows_verified_fetch(url,max_bytes)
            raise
