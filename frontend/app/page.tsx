"use client";
import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  ArrowLeft,
  ArrowRight,
  Bell,
  Building2,
  CheckCircle2,
  Clock3,
  Eye,
  EyeOff,
  FileText,
  Filter,
  Gauge,
  IndianRupee,
  Landmark,
  LayoutDashboard,
  LockKeyhole,
  LogOut,
  MapPin,
  Menu,
  Search,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  UserRound,
  Users,
  X,
} from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Switch } from "@/components/ui/switch";
import LeafletProjectMap from "./leaflet-map";

type Risk = "HIGH" | "MEDIUM" | "LOW";
type Barrier = {
  category: string;
  title: string;
  severity: string;
  impact_score: number | null;
  status: string | null;
  description: string | null;
  mitigation: string | null;
  source_name: string | null;
  source_url: string | null;
  verification_status: string;
  observed_at: string | null;
};
type Project = {
  id: string;
  name: string;
  route: string;
  state: string;
  district: string;
  stage: string;
  compensation: number;
  probability: number;
  risk: Risk;
  families: number;
  land: number;
  possession: number;
  days: number;
  factors: { label: string; value: number; note: string }[];
  actions: string[];
  barriers?: Barrier[];
};
const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_BASE_URL || ""
).replace(/\/$/, "");
const syntheticProjects: Project[] = [
  {
    id: "LA-MH-0125",
    name: "Nashik–Pune Greenfield Corridor",
    route: "NH 60 · Package III",
    state: "Maharashtra",
    district: "Nashik",
    stage: "Compensation",
    compensation: 54,
    probability: 82,
    risk: "HIGH",
    families: 274,
    land: 125.4,
    possession: 32,
    days: 127,
    factors: [
      {
        label: "Compensation pending",
        value: 88,
        note: "46% payment remains incomplete",
      },
      {
        label: "Legal dispute",
        value: 74,
        note: "3 active cases affect possession",
      },
      {
        label: "Stage duration",
        value: 66,
        note: "37 days above expected duration",
      },
      {
        label: "R&R progress",
        value: 52,
        note: "Progress is currently at 41%",
      },
    ],
    actions: [
      "Prioritize compensation verification and payment",
      "Escalate the three unresolved legal cases",
      "Schedule a joint CALA and R&R progress review",
    ],
  },
  {
    id: "LA-MH-0188",
    name: "Mumbai–Vadodara Expressway Spur",
    route: "NE 4 · Package IX",
    state: "Maharashtra",
    district: "Palghar",
    stage: "Possession",
    compensation: 84,
    probability: 68,
    risk: "HIGH",
    families: 186,
    land: 89.2,
    possession: 64,
    days: 93,
    factors: [
      {
        label: "Possession pending",
        value: 78,
        note: "36% land remains to be possessed",
      },
      { label: "Legal dispute", value: 61, note: "2 active cases remain" },
      {
        label: "Stage duration",
        value: 48,
        note: "Possession stage slowed recently",
      },
    ],
    actions: [
      "Conduct parcel-level possession review",
      "Assign legal follow-up for disputed parcels",
      "Verify completed compensation cases",
    ],
  },
  {
    id: "LA-GJ-0074",
    name: "Ahmedabad Ring Road Expansion",
    route: "SH 41 · Eastern arc",
    state: "Gujarat",
    district: "Ahmedabad",
    stage: "R&R",
    compensation: 77,
    probability: 56,
    risk: "MEDIUM",
    families: 318,
    land: 142.8,
    possession: 48,
    days: 74,
    factors: [
      {
        label: "R&R progress",
        value: 69,
        note: "Large number of affected families",
      },
      {
        label: "Possession pending",
        value: 44,
        note: "52% possession remains",
      },
    ],
    actions: [
      "Increase weekly R&R case resolution",
      "Coordinate village-level documentation camp",
    ],
  },
  {
    id: "LA-UP-0211",
    name: "Ganga Expressway Link Road",
    route: "Package II · Link 6",
    state: "Uttar Pradesh",
    district: "Prayagraj",
    stage: "Award",
    compensation: 72,
    probability: 47,
    risk: "MEDIUM",
    families: 229,
    land: 103.7,
    possession: 51,
    days: 61,
    factors: [
      {
        label: "Award processing",
        value: 62,
        note: "Award completion is uneven",
      },
      { label: "Compensation pending", value: 43, note: "28% payment remains" },
    ],
    actions: [
      "Complete pending award documentation",
      "Prepare compensation disbursement schedule",
    ],
  },
  {
    id: "LA-KA-0092",
    name: "Bengaluru Satellite Town Ring Road",
    route: "NH 948A · Package I",
    state: "Karnataka",
    district: "Ramanagara",
    stage: "Compensation",
    compensation: 81,
    probability: 38,
    risk: "MEDIUM",
    families: 143,
    land: 77.9,
    possession: 57,
    days: 48,
    factors: [
      { label: "Compensation pending", value: 45, note: "19% payment remains" },
      {
        label: "Documentation",
        value: 34,
        note: "Some parcel records need verification",
      },
    ],
    actions: [
      "Close remaining parcel verifications",
      "Continue fortnightly compensation review",
    ],
  },
  {
    id: "LA-MP-0046",
    name: "Indore–Harda Highway Widening",
    route: "NH 47 · Package IV",
    state: "Madhya Pradesh",
    district: "Dewas",
    stage: "Possession",
    compensation: 96,
    probability: 22,
    risk: "LOW",
    families: 98,
    land: 51.3,
    possession: 89,
    days: 24,
    factors: [
      {
        label: "Possession pending",
        value: 24,
        note: "11% possession remains",
      },
      {
        label: "Minor documentation",
        value: 16,
        note: "Four parcels under verification",
      },
    ],
    actions: [
      "Complete remaining possession records",
      "Prepare acquisition closure report",
    ],
  },
  {
    id: "LA-RJ-0133",
    name: "Jaipur Northern Bypass",
    route: "NH 52 · Package V",
    state: "Rajasthan",
    district: "Jaipur",
    stage: "Possession",
    compensation: 98,
    probability: 14,
    risk: "LOW",
    families: 76,
    land: 48.6,
    possession: 94,
    days: 19,
    factors: [
      {
        label: "Minor possession gap",
        value: 17,
        note: "6% possession remains",
      },
    ],
    actions: [
      "Close residual possession cases",
      "Begin final compliance review",
    ],
  },
];

function normalizeRisk(rawRisk: string | undefined, fallback: Risk): Risk {
  const normalized = String(rawRisk || fallback).toUpperCase();
  return normalized === "HIGH" || normalized === "MEDIUM" || normalized === "LOW"
    ? (normalized as Risk)
    : fallback;
}

function normalizeProject(record: any, index: number): Project {
  const template = syntheticProjects[index % syntheticProjects.length];
  const barriers: Barrier[] = Array.isArray(record.barriers) ? record.barriers : [];
  const barrierFactors = barriers
    .filter((barrier) => Number.isFinite(Number(barrier.impact_score)))
    .map((barrier) => ({
      label: barrier.title,
      value: Math.round(Number(barrier.impact_score)),
      note: `${barrier.status || "Project condition"} · ${barrier.verification_status}`,
    }));
  const probability =
    record.delay_probability == null
      ? template.probability
      : Math.round(Number(record.delay_probability) * 100);
  const compensation =
    record.compensation_percentage == null
      ? template.compensation
      : Number(record.compensation_percentage);

  return {
    ...template,
    id: String(record.project_id || template.id),
    name: String(record.project_name || template.name),
    route: String(record.project_type || template.route),
    state: String(record.state || template.state),
    district: String(record.district || template.district),
    stage: String(record.current_stage || template.stage),
    compensation: Number.isFinite(compensation) ? compensation : template.compensation,
    probability,
    risk: normalizeRisk(record.risk_level, template.risk),
    families:
      record.affected_families == null
        ? template.families
        : Number(record.affected_families),
    land:
      record.land_required_ha == null ? template.land : Number(record.land_required_ha),
    possession:
      record.possession_percentage == null
        ? template.possession
        : Number(record.possession_percentage),
    days:
      record.days_in_current_stage == null
        ? template.days
        : Number(record.days_in_current_stage),
    factors: barrierFactors.length ? barrierFactors : template.factors,
    barriers,
  };
}

async function loadProjects(): Promise<Project[]> {
  const response = await fetch(`${API_BASE_URL}/api/projects?limit=100`);
  if (!response.ok) throw new Error(`Projects API returned ${response.status}`);

  const payload = await response.json();
  const records = Array.isArray(payload?.projects) ? payload.projects : [];

  return records.map((record: any, index: number) => normalizeProject(record, index));
}
const colors: Record<Risk, string> = {
  HIGH: "#ef6262",
  MEDIUM: "#d89635",
  LOW: "#24a579",
};
function Badge({ risk }: { risk: Risk }) {
  return (
    <span className={`badge ${risk.toLowerCase()}`}>
      <i />
      {risk}
    </span>
  );
}
function Ring({
  value,
  risk,
  small = false,
}: {
  value: number;
  risk: Risk;
  small?: boolean;
}) {
  return (
    <div
      className={`ring ${small ? "small" : ""}`}
      style={{
        background: `conic-gradient(${colors[risk]} ${value * 3.6}deg,#e8eeed 0)`,
      }}
    >
      <div>
        <strong>{value}%</strong>
        {!small && <span>delay risk</span>}
      </div>
    </div>
  );
}
export default function Home() {
  const [auth, setAuth] = useState<"login" | "signup" | "app">("login"),
    [role, setRole] = useState<"civilian" | "official">("official");
  const [view, setView] = useState("dashboard"),
    [query, setQuery] = useState(""),
    [filter, setFilter] = useState("ALL"),
    [allProjects, setAllProjects] = useState<Project[]>(syntheticProjects),
    [selected, setSelected] = useState(syntheticProjects[0]),
    [menu, setMenu] = useState(false),
    [comp, setComp] = useState(syntheticProjects[0].compensation);
  useEffect(() => {
    loadProjects().then((loaded) => {
      if (!loaded.length) return;
      setAllProjects(loaded);
      setSelected(loaded[0]);
      setComp(loaded[0].compensation);
    }).catch((error) => {
      console.warn("Using synthetic project data because the backend is unavailable:", error);
    });
  }, []);
  const rows = useMemo(
    () =>
      allProjects.filter(
        (p) =>
          (filter === "ALL" || p.risk === filter) &&
          `${p.name} ${p.district} ${p.id}`
            .toLowerCase()
            .includes(query.toLowerCase()),
      ),
    [allProjects, query, filter],
  );
  const open = (p: Project) => {
    setSelected(p);
    setComp(p.compensation);
    setView("analysis");
    scrollTo({ top: 0, behavior: "smooth" });
  };
  if (auth !== "app")
    return (
      <AuthScreen
        mode={auth}
        role={role}
        setRole={setRole}
        setMode={setAuth}
        enter={() => setAuth("app")}
      />
    );
  if (role === "civilian")
    return <CivilianApp projects={allProjects} signOut={() => setAuth("login")} />;
  return (
    <div className="shell">
      <aside className={menu ? "open" : ""}>
        <div className="brand">
          <b>
            <Building2 />
          </b>
          <div>
            <strong>
              Bhoomi<span>Drishti</span>
            </strong>
            <small>Early Warning System</small>
          </div>
          <button onClick={() => setMenu(false)}>
            <X />
          </button>
        </div>
        <nav>
          <button
            className={view === "dashboard" ? "active" : ""}
            onClick={() => {
              setView("dashboard");
              setMenu(false);
            }}
          >
            <LayoutDashboard />
            Overview
          </button>
          <button
            className={view === "projects" ? "active" : ""}
            onClick={() => {
              setView("projects");
              setMenu(false);
            }}
          >
            <FileText />
            Projects
          </button>
          <button
            className={view === "analysis" ? "active" : ""}
            onClick={() => {
              setView("analysis");
              setMenu(false);
            }}
          >
            <Gauge />
            Risk analysis <em>AI</em>
          </button>
        </nav>
        <div className="sidefoot">
          <div>
            <i />
            <span>
              <strong>Demo dataset</strong>
              <small>7 project records</small>
            </span>
          </div>
          <button className="logout" onClick={() => setAuth("login")}>
            <LogOut /> Sign out
          </button>
          <p>SIH 2026 · PS-26017</p>
        </div>
      </aside>
      <main>
        <header>
          <button className="menubtn" onClick={() => setMenu(true)}>
            <Menu />
          </button>
          <div>
            <small>LAND ACQUISITION INTELLIGENCE</small>
            <h1>
              {view === "dashboard"
                ? "Command Overview"
                : view === "projects"
                  ? "Project Registry"
                  : "AI Risk Analysis"}
            </h1>
          </div>
          <div className="account">
            <button>
              <Bell />
              <i />
            </button>
            <b>{role === "official" ? "GO" : "CV"}</b>
            <span>
              <strong>
                {role === "official" ? "Government Official" : "Civilian User"}
              </strong>
              <small>
                {role === "official"
                  ? "Decision support access"
                  : "Public information access"}
              </small>
            </span>
          </div>
        </header>
        {view === "dashboard" && <Dashboard projects={allProjects} open={open} go={setView} />}{" "}
        {view === "projects" && (
          <Projects
            rows={rows}
            query={query}
            setQuery={setQuery}
            filter={filter}
            setFilter={setFilter}
            open={open}
          />
        )}{" "}
        {view === "analysis" && (
          <Analysis
            p={selected}
            comp={comp}
            setComp={setComp}
            back={() => setView("projects")}
          />
        )}
      </main>
    </div>
  );
}

function CivilianApp({ projects, signOut }: { projects: Project[]; signOut: () => void }) {
  const [section, setSection] = useState<
    "home" | "projects" | "notices" | "detail"
  >("home");
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const openPublicProject = (projectId: string) => {
    const project = projects.find((item) => item.id === projectId);
    if (!project) return;
    setSelectedProject(project);
    setSection("detail");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };
  return (
    <div className="shell civilian-shell">
      <aside>
        <div className="brand">
          <b>
            <Building2 />
          </b>
          <div>
            <strong>
              Bhoomi<span>Drishti</span>
            </strong>
            <small>Citizen Information Portal</small>
          </div>
        </div>
        <nav>
          <button
            className={section === "home" ? "active" : ""}
            onClick={() => setSection("home")}
          >
            <LayoutDashboard />
            My area
          </button>
          <button
            className={
              section === "projects" || section === "detail" ? "active" : ""
            }
            onClick={() => setSection("projects")}
          >
            <MapPin />
            Nearby projects
          </button>
          <button
            className={section === "notices" ? "active" : ""}
            onClick={() => setSection("notices")}
          >
            <Bell />
            Public notices
          </button>
        </nav>
        <div className="citizen-help">
          <ShieldCheck />
          <strong>Need assistance?</strong>
          <p>
            Find project information and understand the acquisition process.
          </p>
          <button>View citizen guide</button>
        </div>
        <div className="sidefoot">
          <button className="logout" onClick={signOut}>
            <LogOut /> Sign out
          </button>
          <p>SIH 2026 · PUBLIC PORTAL</p>
        </div>
      </aside>
      <main>
        <header>
          <div>
            <small>CITIZEN LAND INFORMATION</small>
            <h1>
              {section === "home"
                ? "Your Area Overview"
                : section === "projects"
                  ? "Nearby Projects"
                  : section === "detail"
                    ? "Project Details"
                    : "Public Notices"}
            </h1>
          </div>
          <div className="account">
            <b>CV</b>
            <span>
              <strong>Civilian User</strong>
              <small>Public information access</small>
            </span>
          </div>
        </header>
        <div className="content civilian-content">
          {section === "home" && (
            <>
              <section className="citizen-hero">
                <div>
                  <span className="eyebrow">PUBLIC INFORMATION</span>
                  <h2>
                    Know what is happening
                    <br />
                    in <i>your area.</i>
                  </h2>
                  <p>
                    Explore nearby land-acquisition projects, understand their
                    current stage, and find official public notices in one
                    place.
                  </p>
                </div>
                <button>
                  <MapPin />
                  Use my location
                </button>
              </section>
              <section className="citizen-kpis">
                <Kpi
                  icon={<MapPin />}
                  label="Nearby projects"
                  value="03"
                  note="Within selected area"
                />
                <Kpi
                  icon={<FileText />}
                  label="New notices"
                  value="02"
                  note="Published this month"
                  tone="amber"
                />
                <Kpi
                  icon={<CheckCircle2 />}
                  label="Open enquiries"
                  value="01"
                  note="Awaiting response"
                  tone="green"
                />
              </section>
              <section className="civilian-grid">
                <article className="panel public-map-panel">
                  <Title
                    over="PROJECT EXPLORER"
                    title="Projects near you"
                    action={<span className="public-pill">Public view</span>}
                  />
                  <LeafletProjectMap
                    audience="civilian"
                    onProjectSelect={openPublicProject}
                  />
                  <p className="map-note">
                    Select a marker to view the public project status. Sensitive
                    administrative data is not displayed.
                  </p>
                </article>
                <CitizenNotices />
              </section>
            </>
          )}
          {section === "projects" && (
            <>
              <section className="pagelead">
                <div>
                  <span className="eyebrow">PUBLIC PROJECT DIRECTORY</span>
                  <h2>Projects near your district</h2>
                  <p>
                    Clear, verified stage information without internal risk or
                    administrative records.
                  </p>
                </div>
              </section>
              <article className="panel public-map-panel full">
                <LeafletProjectMap
                  audience="civilian"
                  onProjectSelect={openPublicProject}
                />
              </article>
              <div className="citizen-project-list">
                {projects.slice(0, 4).map((p) => (
                  <article key={p.id}>
                    <span className="stagetag">{p.stage}</span>
                    <h3>{p.name}</h3>
                    <p>
                      <MapPin />
                      {p.district}, {p.state}
                    </p>
                    <div>
                      <span>Compensation progress</span>
                      <strong>{p.compensation}%</strong>
                    </div>
                    <button onClick={() => openPublicProject(p.id)}>
                      View public details <ArrowRight />
                    </button>
                  </article>
                ))}
              </div>
            </>
          )}
          {section === "notices" && (
            <>
              <section className="pagelead">
                <div>
                  <span className="eyebrow">OFFICIAL UPDATES</span>
                  <h2>Public notices</h2>
                  <p>
                    Notifications, hearings and public information related to
                    monitored projects.
                  </p>
                </div>
              </section>
              <CitizenNotices expanded />
            </>
          )}
          {section === "detail" && selectedProject && (
            <CivilianProjectDetail
              project={selectedProject}
              back={() => setSection("projects")}
            />
          )}
        </div>
      </main>
    </div>
  );
}

function CivilianProjectDetail({
  project,
  back,
}: {
  project: Project;
  back: () => void;
}) {
  const stageUpdates: Record<string, { status: string; next: string }> = {
    Notification: {
      status: "The project notification has been published for public review.",
      next: "Survey and land-record verification will follow.",
    },
    Award: {
      status: "Award documentation and ownership records are being processed.",
      next: "Compensation cases will move to verification and payment.",
    },
    Compensation: {
      status: "Compensation verification and disbursement are in progress.",
      next: "Pending claims will be verified before possession proceeds.",
    },
    "R&R": {
      status: "Rehabilitation and resettlement cases are under review.",
      next: "Eligible cases will be resolved according to the approved plan.",
    },
    Possession: {
      status: "Land possession and final record updates are in progress.",
      next: "Remaining parcels will be closed after document verification.",
    },
  };
  const update = stageUpdates[project.stage] ?? {
    status: "The project is progressing through the acquisition process.",
    next: "The next verified update will be published here.",
  };

  return (
    <section className="civilian-project-detail">
      <button className="back" onClick={back}>
        <ArrowLeft /> Back to nearby projects
      </button>
      <article className="public-detail-hero">
        <div>
          <span className="eyebrow">PUBLIC PROJECT RECORD · {project.id}</span>
          <h2>{project.name}</h2>
          <p>
            <MapPin /> {project.district}, {project.state} · {project.route}
          </p>
        </div>
        <span className="public-stage">{project.stage}</span>
      </article>
      <div className="public-detail-grid">
        <article className="panel public-progress-card">
          <Title over="CURRENT PROGRESS" title="Acquisition update" />
          <div className="public-progress-value">
            <span>Compensation completed</span>
            <strong>{project.compensation}%</strong>
          </div>
          <div className="public-progress-bar">
            <i style={{ width: `${project.compensation}%` }} />
          </div>
          <p>{update.status}</p>
        </article>
        <article className="panel public-next-card">
          <Title over="WHAT HAPPENS NEXT" title="Expected next step" />
          <div>
            <CheckCircle2 />
            <p>{update.next}</p>
          </div>
          <small>
            Information shown here is the latest published public status.
          </small>
        </article>
      </div>
      <article className="grievance-box detail-enquiry">
        <CircleHelpIcon />
        <div>
          <strong>Have a question about this project?</strong>
          <small>Submit an enquiry mentioning project ID {project.id}.</small>
        </div>
        <button>Raise enquiry</button>
      </article>
    </section>
  );
}

function CitizenNotices({ expanded = false }: { expanded?: boolean }) {
  const notices = [
    {
      date: "28 AUG 2026",
      title: "Compensation verification camp",
      place: "Nashik · Taluka Office",
      type: "Public camp",
    },
    {
      date: "24 AUG 2026",
      title: "Stakeholder hearing schedule",
      place: "Palghar · District Hall",
      type: "Hearing",
    },
    {
      date: "18 AUG 2026",
      title: "Updated possession notice",
      place: "Ahmedabad · Eastern Zone",
      type: "Notification",
    },
  ];
  const loopingNotices = [...notices, ...notices];
  return (
    <article className={`panel citizen-notices ${expanded ? "expanded" : ""}`}>
      <Title over="LATEST UPDATES" title="Public notices" />
      <div className="notice-ticker" aria-label="Latest public notices">
        <div className="notice-track">
          {loopingNotices.map((n, index) => {
            const duplicate = index >= notices.length;
            return (
              <button
                key={`${n.title}-${index}`}
                aria-hidden={duplicate}
                tabIndex={duplicate ? -1 : 0}
              >
                <span>{n.date}</span>
                <div>
                  <strong>{n.title}</strong>
                  <small>{n.place}</small>
                </div>
                <em>{n.type}</em>
                <ArrowRight />
              </button>
            );
          })}
        </div>
      </div>
      <div className="grievance-box">
        <CircleHelpIcon />
        <div>
          <strong>Have a project-related question?</strong>
          <small>Submit an enquiry and track its response.</small>
        </div>
        <button>Raise enquiry</button>
      </div>
    </article>
  );
}
function CircleHelpIcon() {
  return <span className="help-icon">?</span>;
}

function AuthScreen({
  mode,
  role,
  setRole,
  setMode,
  enter,
}: {
  mode: "login" | "signup";
  role: "civilian" | "official";
  setRole: (r: "civilian" | "official") => void;
  setMode: (m: "login" | "signup") => void;
  enter: () => void;
}) {
  const [show, setShow] = useState(false),
    [robot, setRobot] = useState(false),
    [error, setError] = useState(""),
    [email, setEmail] = useState(""),
    [password, setPassword] = useState("");
  const demo =
    role === "official"
      ? { email: "umang.gov@officials.in", password: "Official@123" }
      : { email: "citizen@bhoomidrishti.in", password: "Citizen@123" };
  const changeRole = (next: "civilian" | "official") => {
    setRole(next);
    setError("");
    setEmail("");
    setPassword("");
    setRobot(false);
  };
  const fillDemo = () => {
    setEmail(demo.email);
    setPassword(demo.password);
    setRobot(true);
    setError("");
  };
  const submit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (
      role === "official" &&
      !/^[a-z][a-z0-9._-]*\.gov@officials\.in$/i.test(email)
    ) {
      setError("Use your official email in the format name.gov@officials.in");
      return;
    }
    if (!robot) {
      setError("Please complete the verification checkbox.");
      return;
    }
    if (mode === "signup" && role === "official") {
      setError("Government accounts are issued only to approved officials.");
      return;
    }
    setError("");
    try {
      const formData = new FormData(e.currentTarget);
      const response = await fetch(`${API_BASE_URL}/api/auth/${mode}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          password,
          role,
          full_name: formData.get("full_name"),
        }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || "Authentication failed.");
      if (mode === "signup") {
        setMode("login");
        setPassword("");
        setRobot(false);
        setError("Account created. Please sign in.");
      } else {
        enter();
      }
    } catch (authError) {
      setError(authError instanceof Error ? authError.message : "Authentication failed.");
    }
  };
  return (
    <main className="authpage">
      <section className="authvisual">
        <div className="mapgrid" />
        <div className="maplines">
          <span />
          <span />
          <span />
          <span />
        </div>
        <div className="mapdot one" />
        <div className="mapdot two" />
        <div className="mapdot three" />
        <div className="visualbrand">
          <div className="brandseal">
            <Building2 />
          </div>
          <h1>
            <span className="bhoomiword">Bhoomi</span>
            <span className="drishtiword">Drishti</span>
          </h1>
          <p>Land Acquisition Early Warning System</p>
          <MiniRiskMap />
          <div className="visualtag">
            <ShieldCheck /> Transparent data. Timely intervention.
          </div>
        </div>
        <div className="visualfooter">SIH 2026 · PS-26017</div>
      </section>
      <section className="authside">
        <div className={`authcard ${mode}`}>
          <div className="authmobilebrand">
            <Building2 />
            <strong>BhoomiDrishti</strong>
          </div>
          <span className="authover">SECURE ACCESS PORTAL</span>
          <h2>{mode === "login" ? "Sign in" : "Create your account"}</h2>
          <p>
            {mode === "login"
              ? "Access land acquisition insights and verified project information."
              : "Choose your user type and provide the required verification details."}
          </p>
          <div className="rolepicker">
            <button
              type="button"
              className={role === "civilian" ? "active" : ""}
              onClick={() => changeRole("civilian")}
            >
              <UserRound />
              Civilian
            </button>
            <button
              type="button"
              className={role === "official" ? "active" : ""}
              onClick={() => changeRole("official")}
            >
              <Landmark />
              Government official
            </button>
          </div>
          {mode === "login" && (
            <div className="demoaccount">
              <div>
                <span>
                  DEMO {role === "official" ? "OFFICIAL" : "CIVILIAN"} ACCOUNT
                </span>
                <strong>{demo.email}</strong>
                <small>Password: {demo.password}</small>
              </div>
              <button type="button" onClick={fillDemo}>
                Use demo account
              </button>
            </div>
          )}
          <form onSubmit={submit}>
            {mode === "signup" && <SignupFields role={role} />}
            <label className="field">
              <span>
                {role === "official"
                  ? "Official government email"
                  : "Email address"}
              </span>
              <div>
                <UserRound />
                <input
                  name="email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder={
                    role === "official"
                      ? "umang.gov@officials.in"
                      : "name@example.com"
                  }
                />
              </div>
              {role === "official" && (
                <small>Required format: name.gov@officials.in</small>
              )}
            </label>
            <label className="field">
              <span>Password</span>
              <div>
                <LockKeyhole />
                <input
                  name="password"
                  type={show ? "text" : "password"}
                  minLength={8}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  aria-label="Show password"
                  onClick={() => setShow(!show)}
                >
                  {show ? <EyeOff /> : <Eye />}
                </button>
              </div>
            </label>
            {mode === "signup" && (
              <label className="field">
                <span>Confirm password</span>
                <div>
                  <LockKeyhole />
                  <input
                    type={show ? "text" : "password"}
                    minLength={8}
                    required
                    placeholder="Re-enter your password"
                  />
                </div>
              </label>
            )}
            <div className="captcha">
              <input
                className="native-check"
                id="robot"
                type="checkbox"
                checked={robot}
                onChange={(e) => setRobot(e.target.checked)}
              />
              <label htmlFor="robot">I’m not a robot</label>
              <div>
                <ShieldCheck />
                <small>
                  PROTOTYPE
                  <br />
                  VERIFICATION
                </small>
              </div>
            </div>
            {error && (
              <div className="autherror">
                <AlertTriangle />
                {error}
              </div>
            )}
            {mode === "login" && (
              <div className="loginextras">
                <label>
                  <input className="native-check small" type="checkbox" /> Keep
                  me signed in
                </label>
                <button type="button">Forgot password?</button>
              </div>
            )}
            <button className="primaryauth" type="submit">
              {mode === "login" ? "Sign in securely" : "Create account"}
              <ArrowRight />
            </button>
          </form>
          <div className="authswitch">
            {mode === "login"
              ? "New to BhoomiDrishti?"
              : "Already have an account?"}{" "}
            <button
              onClick={() => {
                setMode(mode === "login" ? "signup" : "login");
                setError("");
              }}
            >
              {mode === "login" ? "Sign up" : "Sign in"}
            </button>
          </div>
          <small className="privacy">
            By continuing, you agree to the platform’s Terms of Use and Privacy
            Policy.
          </small>
        </div>
      </section>
    </main>
  );
}

const miniLocations = [
  {
    name: "Nashik",
    stage: "Compensation",
    risk: "High",
    x: 27,
    y: 31,
    tone: "high",
  },
  {
    name: "Palghar",
    stage: "Possession",
    risk: "High",
    x: 20,
    y: 52,
    tone: "high",
  },
  {
    name: "Jaipur",
    stage: "Possession",
    risk: "Low",
    x: 45,
    y: 22,
    tone: "low",
  },
  {
    name: "Prayagraj",
    stage: "Award",
    risk: "Medium",
    x: 68,
    y: 42,
    tone: "medium",
  },
];
function MiniRiskMap() {
  const [active, setActive] = useState(0);
  useEffect(() => {
    const timer = window.setInterval(
      () => setActive((v) => (v + 1) % miniLocations.length),
      2600,
    );
    return () => window.clearInterval(timer);
  }, []);
  const place = miniLocations[active];
  return (
    <div className="minimap" aria-label="Interactive project risk map">
      <div className="minimaphead">
        <span>
          <MapPin />
          LIVE PROJECT MAP
        </span>
        <small>Hover or tap a marker</small>
      </div>
      <div className="mapcanvas">
        <div className="scanline" />
        <div className="mapshape">
          <i />
          <i />
          <i />
          <i />
        </div>
        <div className="routewave one" />
        <div className="routewave two" />
        {miniLocations.map((p, i) => (
          <button
            key={p.name}
            type="button"
            aria-label={`View ${p.name}`}
            className={`projectpin ${p.tone} ${active === i ? "active" : ""}`}
            style={{ left: `${p.x}%`, top: `${p.y}%` }}
            onClick={() => setActive(i)}
            onMouseEnter={() => setActive(i)}
          >
            <span />
          </button>
        ))}
        <div className="mapinfo" key={place.name}>
          <span className={place.tone} />
          <div>
            <strong>{place.name}</strong>
            <small>
              {place.stage} · {place.risk} risk
            </small>
          </div>
        </div>
      </div>
      <div className="maplegend">
        <span>
          <i className="high" />
          High
        </span>
        <span>
          <i className="medium" />
          Medium
        </span>
        <span>
          <i className="low" />
          Low
        </span>
        <b>Auto-scanning projects</b>
      </div>
    </div>
  );
}
function SignupFields({ role }: { role: "civilian" | "official" }) {
  return (
    <div className="signupgrid">
      <label className="field">
        <span>Full name</span>
        <input name="full_name" required placeholder="As per government ID" />
      </label>
      <label className="field">
        <span>Age</span>
        <input type="number" min="18" max="100" required placeholder="Age" />
      </label>
      <label className="field">
        <span>Gender</span>
        <select required defaultValue="">
          <option value="" disabled>
            Select gender
          </option>
          <option>Female</option>
          <option>Male</option>
          <option>Non-binary</option>
          <option>Prefer not to say</option>
        </select>
      </label>
      {role === "official" ? (
        <>
          <label className="field">
            <span>Government ID number</span>
            <input required placeholder="Employee / service ID" />
          </label>
          <label className="field">
            <span>Government branch</span>
            <select required defaultValue="">
              <option value="" disabled>
                Select branch
              </option>
              <option>Central Government</option>
              <option>State Government</option>
              <option>District Administration</option>
              <option>Local Authority</option>
              <option>Public Sector Agency</option>
            </select>
          </label>
          <label className="field">
            <span>Government sector</span>
            <select required defaultValue="">
              <option value="" disabled>
                Select sector
              </option>
              <option>Roads & Highways</option>
              <option>Railways</option>
              <option>Urban Development</option>
              <option>Irrigation</option>
              <option>Revenue & Land Records</option>
              <option>Other Infrastructure</option>
            </select>
          </label>
        </>
      ) : (
        <>
          <label className="field">
            <span>Mobile number</span>
            <input
              type="tel"
              required
              pattern="[0-9]{10}"
              placeholder="10-digit number"
            />
          </label>
          <label className="field">
            <span>Identity document</span>
            <select required defaultValue="">
              <option value="" disabled>
                Select document
              </option>
              <option>Aadhaar</option>
              <option>Voter ID</option>
              <option>Driving Licence</option>
              <option>Passport</option>
            </select>
          </label>
          <label className="field">
            <span>State / Union Territory</span>
            <input required placeholder="Your state" />
          </label>
        </>
      )}
    </div>
  );
}
function Dashboard({
  projects,
  open,
  go,
}: {
  projects: Project[];
  open: (p: Project) => void;
  go: (s: string) => void;
}) {
  return (
    <div className="content">
      <section className="intro">
        <div>
          <span className="eyebrow">OFFICIAL INTELLIGENCE</span>
          <h2>
            See delays before
            <br />
            they become <i>roadblocks.</i>
          </h2>
          <p>
            Detailed project intelligence to identify acquisition risk,
            understand its causes, and prioritize administrative action.
          </p>
        </div>
        <div className="updated">
          <Clock3 />
          Model snapshot
          <br />
          <strong>30 Aug 2026 · 14:30</strong>
        </div>
      </section>
      <section className="kpis">
        <Kpi
          icon={<FileText />}
          label="Projects monitored"
          value="07"
          note="Across 6 districts"
        />
        <Kpi
          icon={<ShieldAlert />}
          label="High risk"
          value="02"
          note="Needs intervention"
          tone="red"
        />
        <Kpi
          icon={<AlertTriangle />}
          label="Medium risk"
          value="03"
          note="Watch closely"
          tone="amber"
        />
        <Kpi
          icon={<CheckCircle2 />}
          label="Low risk"
          value="02"
          note="On expected path"
          tone="green"
        />
      </section>
      <section className="grid">
        <article className="panel official-map-panel">
          <Title
            over="GIS RISK INTELLIGENCE"
            title="National project risk map"
            action={<span className="official-pill">Official detail</span>}
          />
          <LeafletProjectMap
            audience="official"
            onProjectSelect={(projectId) => {
              const project = projects.find((item) => item.id === projectId);
              if (project) open(project);
            }}
          />
          <p className="map-note">
            Markers display model risk, delay probability, acquisition stage and
            compensation progress.
          </p>
        </article>
        <article className="panel distribution">
          <Title
            over="PORTFOLIO HEALTH"
            title="Risk distribution"
            action={
              <button onClick={() => go("projects")}>
                View all <ArrowRight />
              </button>
            }
          />
          <div className="donutrow">
            <div className="donut">
              <div>
                <strong>7</strong>
                <span>projects</span>
              </div>
            </div>
            <div className="legend">
              <Legend risk="HIGH" value="2" percent="29%" />
              <Legend risk="MEDIUM" value="3" percent="43%" />
              <Legend risk="LOW" value="2" percent="28%" />
            </div>
          </div>
        </article>
        <article className="panel stages">
          <Title over="PROCESS VIEW" title="Acquisition stages" />
          <Stage name="Notification" value={7} />
          <Stage name="Award" value={6} />
          <Stage name="Compensation" value={5} />
          <Stage name="R&R" value={4} />
          <Stage name="Possession" value={3} />
        </article>
        <article className="panel priority">
          <Title
            over="REQUIRES ATTENTION"
            title="Priority interventions"
            action={<span className="urgent">2 urgent</span>}
          />
          {projects.slice(0, 2).map((p, i) => (
            <button className="priorityrow" onClick={() => open(p)} key={p.id}>
              <span>0{i + 1}</span>
              <div>
                <strong>{p.name}</strong>
                <small>
                  <MapPin />
                  {p.district} · {p.stage}
                </small>
                <i>
                  <b style={{ width: `${p.probability}%` }} />
                </i>
              </div>
              <em>
                <strong>{p.probability}%</strong>
                <small>risk</small>
              </em>
              <ArrowRight />
            </button>
          ))}
        </article>
        <article className="insight">
          <Sparkles />
          <div>
            <small>AI PORTFOLIO INSIGHT</small>
            <h3>Compensation is the leading controllable risk.</h3>
            <p>
              It appears among the top three risk factors in 4 of 7 monitored
              projects.
            </p>
            <button onClick={() => open(projects[0])}>
              Explore analysis <ArrowRight />
            </button>
          </div>
        </article>
      </section>
    </div>
  );
}
function Projects({
  rows,
  query,
  setQuery,
  filter,
  setFilter,
  open,
}: {
  rows: Project[];
  query: string;
  setQuery: (s: string) => void;
  filter: string;
  setFilter: (s: string) => void;
  open: (p: Project) => void;
}) {
  return (
    <div className="content">
      <section className="pagelead">
        <div>
          <span className="eyebrow">MASTER DATASET</span>
          <h2>Monitored projects</h2>
          <p>
            Review acquisition progress and open any project for its complete
            risk explanation.
          </p>
        </div>
        <span>{rows.length} records</span>
      </section>
      <div className="toolbar">
        <label>
          <Search />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search project, district or ID…"
          />
        </label>
        <label className="select">
          <Filter />
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="ALL">All risk levels</option>
            <option>HIGH</option>
            <option>MEDIUM</option>
            <option>LOW</option>
          </select>
        </label>
      </div>
      <div className="table">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Project</TableHead>
              <TableHead>Location</TableHead>
              <TableHead>Current stage</TableHead>
              <TableHead>Compensation</TableHead>
              <TableHead>Risk</TableHead>
              <TableHead />
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.map((p) => (
              <TableRow onClick={() => open(p)} key={p.id}>
                <TableCell>
                  <strong>{p.name}</strong>
                  <small>
                    {p.id} · {p.route}
                  </small>
                </TableCell>
                <TableCell>
                  <strong>{p.district}</strong>
                  <small>{p.state}</small>
                </TableCell>
                <TableCell>
                  <span className="stagetag">{p.stage}</span>
                </TableCell>
                <TableCell>
                  <div className="progress">
                    <i>
                      <b style={{ width: `${p.compensation}%` }} />
                    </i>
                    <strong>{p.compensation}%</strong>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="riskcell">
                    <Badge risk={p.risk} />
                    <strong>{p.probability}%</strong>
                  </div>
                </TableCell>
                <TableCell>
                  <button>
                    <ArrowRight />
                  </button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {!rows.length && (
          <div className="empty">
            <Search />
            <h3>No matching projects</h3>
            <p>Try another search term or risk filter.</p>
          </div>
        )}
      </div>
    </div>
  );
}
function Analysis({
  p,
  comp,
  setComp,
  back,
}: {
  p: Project;
  comp: number;
  setComp: (n: number) => void;
  back: () => void;
}) {
  type ScenarioFactor =
    | "compensation"
    | "legal"
    | "duration"
    | "rr"
    | "climate"
    | "landscape"
    | "approvals";
  const [activeFactors, setActiveFactors] = useState<ScenarioFactor[]>([
    "compensation",
  ]);
  const [legalResolution, setLegalResolution] = useState(0);
  const [durationImprovement, setDurationImprovement] = useState(0);
  const [rrProgress, setRrProgress] = useState(41);
  const [climateMitigation, setClimateMitigation] = useState(0);
  const [landscapeMitigation, setLandscapeMitigation] = useState(0);
  const [approvalImprovement, setApprovalImprovement] = useState(0);

  useEffect(() => {
    setActiveFactors(["compensation"]);
    setLegalResolution(0);
    setDurationImprovement(0);
    setRrProgress(41);
    setClimateMitigation(0);
    setLandscapeMitigation(0);
    setApprovalImprovement(0);
    setComp(p.compensation);
  }, [p.id]);

  const isActive = (factor: ScenarioFactor) =>
    activeFactors.includes(factor);
  const setFactorActive = (factor: ScenarioFactor, active: boolean) => {
    setActiveFactors((current) =>
      active
        ? current.includes(factor)
          ? current
          : [...current, factor]
        : current.filter((item) => item !== factor),
    );
  };
  const reduction =
    (isActive("compensation") ? (comp - p.compensation) * 0.35 : 0) +
    (isActive("legal") ? legalResolution * 0.14 : 0) +
    (isActive("duration") ? durationImprovement * 0.1 : 0) +
    (isActive("rr") ? Math.max(0, rrProgress - 41) * 0.17 : 0) +
    (isActive("climate") ? climateMitigation * 0.08 : 0) +
    (isActive("landscape") ? landscapeMitigation * 0.08 : 0) +
    (isActive("approvals") ? approvalImprovement * 0.1 : 0);
  const sim = Math.max(9, Math.round(p.probability - reduction)),
    simRisk: Risk = sim > 60 ? "HIGH" : sim > 30 ? "MEDIUM" : "LOW";
  const scenarioFactors: {
    key: ScenarioFactor;
    label: string;
    note: string;
  }[] = [
    {
      key: "compensation",
      label: "Compensation",
      note: "Payment completion",
    },
    { key: "legal", label: "Legal disputes", note: "Cases resolved" },
    {
      key: "duration",
      label: "Stage duration",
      note: "Delay reduced",
    },
    { key: "rr", label: "R&R progress", note: "Cases completed" },
    {
      key: "climate",
      label: "Climate barriers",
      note: "Weather disruption mitigated",
    },
    {
      key: "landscape",
      label: "Landscape constraints",
      note: "Terrain and access mitigated",
    },
    {
      key: "approvals",
      label: "Approvals",
      note: "Clearance dependency reduced",
    },
  ];
  return (
    <div className="content">
      <button className="back" onClick={back}>
        <ArrowLeft />
        Back to projects
      </button>
      <section className="analysishead">
        <div>
          <span>
            {p.id} · {p.route}
          </span>
          <h2>{p.name}</h2>
          <p>
            <MapPin />
            {p.district}, {p.state} · Current stage: <strong>{p.stage}</strong>
          </p>
        </div>
        <div>
          <Badge risk={p.risk} />
          <Ring value={p.probability} risk={p.risk} />
        </div>
      </section>
      <section className="details">
        <Detail
          icon={<FileText />}
          label="Land required"
          value={`${p.land} ha`}
        />
        <Detail
          icon={<Users />}
          label="Affected families"
          value={`${p.families}`}
        />
        <Detail
          icon={<IndianRupee />}
          label="Compensation"
          value={`${p.compensation}%`}
        />
        <Detail
          icon={<MapPin />}
          label="Possession"
          value={`${p.possession}%`}
        />
        <Detail icon={<Clock3 />} label="Days in stage" value={`${p.days}`} />
      </section>
      <section className="analysisgrid">
        <article className="panel factors">
          <Title
            over="MODEL EXPLANATION"
            title="Why is this project at risk?"
            action={<span className="prototype">Prototype estimate</span>}
          />
          <p>
            Relative influence of available project conditions on the current
            prediction.
          </p>
          {p.factors.map((f, i) => (
            <div className="factor" key={f.label}>
              <span>0{i + 1}</span>
              <div>
                <label>
                  <strong>{f.label}</strong>
                  <b>{f.value}</b>
                </label>
                <i>
                  <b style={{ width: `${f.value}%` }} />
                </i>
                <small>{f.note}</small>
              </div>
            </div>
          ))}
          {p.barriers?.length ? (
            <div className="barrier-list">
              <h4>Project-specific conditions</h4>
              {p.barriers.map((barrier) => (
                <div className="barrier-item" key={`${barrier.category}-${barrier.title}`}>
                  <div>
                    <strong>{barrier.title}</strong>
                    <span>{barrier.category} · {barrier.severity} impact</span>
                  </div>
                  <p>{barrier.description || "No description available."}</p>
                  <small>
                    {barrier.verification_status} · {barrier.observed_at ? `observed ${new Date(barrier.observed_at).toLocaleDateString()}` : "observation date unavailable"}
                    {barrier.source_url && (
                      <> · <a href={barrier.source_url} target="_blank" rel="noreferrer">source</a></>
                    )}
                  </small>
                </div>
              ))}
            </div>
          ) : null}
        </article>
        <article className="panel actions">
          <Title
            over="DECISION SUPPORT"
            title="Recommended actions"
            action={<Sparkles />}
          />
          {p.actions.map((a, i) => (
            <div className="action" key={a}>
              <span>{i + 1}</span>
              <div>
                <strong>{a}</strong>
                <small>{i ? "Follow-up action" : "Immediate priority"}</small>
              </div>
            </div>
          ))}
          <div className="notice">
            <AlertTriangle />
            <p>Recommendations support—not replace—administrative judgment.</p>
          </div>
        </article>
        <article className="panel simulator">
          <div>
            <span className="over">SCENARIO EXPLORER</span>
            <h3>What if key project conditions improve?</h3>
            <p>
              Select one or more model factors, adjust their improvement and
              compare the combined estimate. This is a scenario, not a causal
              guarantee.
            </p>
            <div className="scenario-picker">
              <div className="scenario-picker-head">
                <strong>Factors to improve</strong>
                <span>{activeFactors.length} selected</span>
              </div>
              <div className="scenario-toggles">
                {scenarioFactors.map((factor) => (
                  <label
                    className={isActive(factor.key) ? "active" : ""}
                    key={factor.key}
                  >
                    <Switch
                      className="scenario-switch"
                      checked={isActive(factor.key)}
                      onCheckedChange={(checked) =>
                        setFactorActive(factor.key, checked)
                      }
                      aria-label={`Include ${factor.label} in scenario`}
                    />
                    <span>
                      <strong>{factor.label}</strong>
                      <small>{factor.note}</small>
                    </span>
                  </label>
                ))}
              </div>
            </div>
            <div className="scenario-controls">
              {isActive("compensation") && (
                <ScenarioControl
                  label="Compensation completion"
                  value={comp}
                  min={p.compensation}
                  onChange={setComp}
                  start={`${p.compensation}% current`}
                />
              )}
              {isActive("legal") && (
                <ScenarioControl
                  label="Legal disputes resolved"
                  value={legalResolution}
                  min={0}
                  onChange={setLegalResolution}
                  start="0% resolved"
                />
              )}
              {isActive("duration") && (
                <ScenarioControl
                  label="Stage-duration improvement"
                  value={durationImprovement}
                  min={0}
                  onChange={setDurationImprovement}
                  start="No reduction"
                />
              )}
              {isActive("rr") && (
                <ScenarioControl
                  label="R&R progress"
                  value={rrProgress}
                  min={41}
                  onChange={setRrProgress}
                  start="41% current"
                />
              )}
              {isActive("climate") && (
                <ScenarioControl
                  label="Climate barrier mitigation"
                  value={climateMitigation}
                  min={0}
                  onChange={setClimateMitigation}
                  start="No mitigation"
                />
              )}
              {isActive("landscape") && (
                <ScenarioControl
                  label="Landscape constraint mitigation"
                  value={landscapeMitigation}
                  min={0}
                  onChange={setLandscapeMitigation}
                  start="No mitigation"
                />
              )}
              {isActive("approvals") && (
                <ScenarioControl
                  label="Approval delay improvement"
                  value={approvalImprovement}
                  min={0}
                  onChange={setApprovalImprovement}
                  start="No improvement"
                />
              )}
              {!activeFactors.length && (
                <div className="scenario-empty">
                  Select at least one factor to explore an improvement.
                </div>
              )}
            </div>
          </div>
          <div className="simresult">
            <div>
              <span>CURRENT</span>
              <Ring value={p.probability} risk={p.risk} small />
            </div>
            <ArrowRight />
            <div>
              <span>SIMULATED</span>
              <Ring value={sim} risk={simRisk} small />
            </div>
            <p>
              ↓ {p.probability - sim} percentage-point reduction ·{" "}
              {activeFactors.length} factor
              {activeFactors.length === 1 ? "" : "s"}
            </p>
          </div>
        </article>
      </section>
    </div>
  );
}

function ScenarioControl({
  label,
  value,
  min,
  onChange,
  start,
}: {
  label: string;
  value: number;
  min: number;
  onChange: (value: number) => void;
  start: string;
}) {
  return (
    <div className="scenario-control">
      <label>
        {label} <strong>{value}%</strong>
      </label>
      <input
        type="range"
        min={min}
        max="100"
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        aria-label={label}
      />
      <small>
        {start} <span>100%</span>
      </small>
    </div>
  );
}
function Kpi({
  icon,
  label,
  value,
  note,
  tone = "blue",
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  note: string;
  tone?: string;
}) {
  return (
    <article className={`kpi ${tone}`}>
      <b>{icon}</b>
      <div>
        <span>{label}</span>
        <strong>{value}</strong>
        <small>{note}</small>
      </div>
    </article>
  );
}
function Title({
  over,
  title,
  action,
}: {
  over: string;
  title: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="title">
      <div>
        <small>{over}</small>
        <h3>{title}</h3>
      </div>
      {action}
    </div>
  );
}
function Legend({
  risk,
  value,
  percent,
}: {
  risk: Risk;
  value: string;
  percent: string;
}) {
  return (
    <div>
      <i style={{ background: colors[risk] }} />
      <span>
        <strong>{risk[0] + risk.slice(1).toLowerCase()} risk</strong>
        <small>{percent} of portfolio</small>
      </span>
      <b>{value}</b>
    </div>
  );
}
function Stage({ name, value }: { name: string; value: number }) {
  return (
    <div className="stage">
      <label>
        <span>{name}</span>
        <strong>{value}/7</strong>
      </label>
      <i>
        <b style={{ width: `${(value / 7) * 100}%` }} />
      </i>
    </div>
  );
}
function Detail({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div>
      <span>{icon}</span>
      <label>
        <small>{label}</small>
        <strong>{value}</strong>
      </label>
    </div>
  );
}
