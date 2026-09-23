import { NextResponse } from "next/server";
import { demoProjects } from "@/lib/demo-projects";

export function GET() {
  return NextResponse.json({
    projects: demoProjects.map((project) => ({
      ...project,
      barriers: [],
      evidence: { observation_count: 0, source_count: 0 },
    })),
    total: demoProjects.length,
    limit: 100,
    offset: 0,
    success: true,
  });
}
