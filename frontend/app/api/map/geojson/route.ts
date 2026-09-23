import { NextResponse } from "next/server";
import { demoProjects } from "@/lib/demo-projects";

export function GET() {
  const features = demoProjects.map((project) => ({
    type: "Feature",
    properties: {
      ...project,
      status: `${project.current_stage} stage is being monitored`,
      barriers: [],
    },
    geometry: {
      type: "Point",
      coordinates: [project.longitude, project.latitude],
    },
  }));

  return NextResponse.json({
    type: "FeatureCollection",
    features,
    total_features: features.length,
    success: true,
  });
}
