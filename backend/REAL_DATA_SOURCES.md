# Real Project Data Sources

The `real` loader contains publicly documented infrastructure project identities and project-level coordinates. The source links are stored on every project and exposed by the project detail API.

## Source policy

- Project name, agency, and source links are source-backed.
- Coordinates are project-level map points. They are resolved from OpenStreetMap Nominatim where available and are not parcel boundaries.
- Compensation, legal, social-impact, approval, and delay-risk values are not claimed to be official unless a source-specific record supplies them. The current schema still contains demo analytical fields for compatibility; the `data_status` field identifies this limitation.
- Do not present those analytical fields as official measurements in a public demonstration.

## Sources

| Project group | Official source | Document or project page |
| --- | --- | --- |
| Delhi–Mumbai Expressway, Bharatmala | [NHAI](https://nhai.gov.in/) | [Bharatmala project map PDF](https://nhai.gov.in/assets/pdf/Bharatmala_NH_highlighted_2023_Project.pdf) |
| Ganga Expressway | [UPEIDA](https://upeida.in/) | UPEIDA project portal |
| Char Dham Highway | [MoRTH](https://morth.gov.in/) | MoRTH official portal |
| Mumbai Metro Line 3 | [MMRCL](https://mmrcl.com/) | MMRCL official portal |
| Delhi Metro Phase IV | [DMRC](https://delhimetrorail.com/) | [DMRC about page](https://delhimetrorail.com/pages/en/about_us) |
| Chennai Metro Rail Project | [CMRL](https://chennaimetrorail.org/) | [CMRL project status](https://chennaimetrorail.org/project-status-2/) |
| Zojila Tunnel | [NHIDCL](https://nhidcl.com/) | NHIDCL official portal |
| Mumbai–Nagpur Expressway | [MSRDC](https://www.msrdc.org/) | MSRDC official portal |
| Eastern Dedicated Freight Corridor | [DFCCIL](https://dfccil.com/) | [DFCCIL project pages](https://dfccil.com/Home/DynemicPages?MenuId=76) |

Load the expanded catalog with:

```powershell
Set-Location "C:\Users\admin\Desktop\SIH_Land-Acquisition\backend"
& "..\.venv\Scripts\python.exe" load_data.py --source real
```

The loader stores source snapshots and the API exposes freshness and coverage at `GET /api/data-quality`. Schedule `refresh_real_data.py` with Windows Task Scheduler after choosing a refresh interval. The current official websites do not expose all acquisition metrics as machine-readable data, so those fields remain unavailable rather than fabricated.