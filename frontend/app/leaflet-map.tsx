"use client";

import { useEffect, useRef } from "react";
import type { Map as LeafletMapInstance } from "leaflet";

type MapPoint = {
  id: string;
  name: string;
  district: string;
  lat: number;
  lng: number;
  stage: string;
  risk: "HIGH" | "MEDIUM" | "LOW" | "NO_RISK";
  probability: number;
  compensation: number;
  status: string;
  barriers: { title: string; severity: string }[];
};

const riskColor: Record<string, string> = {
  HIGH: "#ef6262",
  MEDIUM: "#d89635",
  LOW: "#24a579",
  NO_RISK: "#24a579",
};

const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_BASE_URL || ""
).replace(/\/$/, "");

function toMapPoint(feature: any): MapPoint | null {
  if (!feature?.geometry || !feature?.properties) return null;
  const props = feature.properties;
  const coords = Array.isArray(feature.geometry.coordinates)
    ? feature.geometry.coordinates
    : [];
  if (coords.length < 2) return null;

  const lng = Number(coords[0]);
  const lat = Number(coords[1]);
  if (!Number.isFinite(lat) || !Number.isFinite(lng)) return null;

  const riskValue = String(props.risk_level || "LOW").toUpperCase();
  const risk: MapPoint["risk"] =
    riskValue === "HIGH" || riskValue === "MEDIUM" || riskValue === "LOW" || riskValue === "NO_RISK"
      ? (riskValue as MapPoint["risk"])
      : "NO_RISK";

  const probability = Number(props.delay_probability);
  const compensation = Number(props.compensation_percentage ?? 0);
  const barriers = Array.isArray(props.barriers)
    ? props.barriers.map((barrier: any) => ({
        title: String(barrier.title || "Project condition"),
        severity: String(barrier.severity || "MEDIUM"),
      }))
    : [];

  return {
    id: String(props.project_id || "unknown"),
    name: String(props.project_name || "Project"),
    district: String(props.district || "Unknown district"),
    lat,
    lng,
    stage: String(props.current_stage || props.stage || "Active"),
    risk,
    probability: Number.isFinite(probability) ? Math.round(probability * 100) : 0,
    compensation: Number.isFinite(compensation) ? compensation : 0,
    barriers,
    status: String(
      props.status ||
        `${props.stage || props.current_stage || "Project"} record is being monitored`,
    ),
  };
}

export default function LeafletProjectMap({
  audience = "official",
  onProjectSelect,
}: {
  audience?: "official" | "civilian";
  onProjectSelect?: (projectId: string) => void;
}) {
  const container = useRef<HTMLDivElement>(null);
  const mapRef = useRef<LeafletMapInstance | null>(null);
  const selectRef = useRef(onProjectSelect);

  useEffect(() => {
    selectRef.current = onProjectSelect;
  }, [onProjectSelect]);

  useEffect(() => {
    if (!container.current || mapRef.current) return;
    let disposed = false;
    const mapContainer = container.current;
    const openProject = (event: MouseEvent) => {
      const target = (event.target as HTMLElement).closest<HTMLElement>(
        "[data-project-id]",
      );
      const projectId = target?.dataset.projectId;
      if (projectId) selectRef.current?.(projectId);
    };
    mapContainer.addEventListener("click", openProject);

    import("leaflet").then((L) => {
      if (disposed || !container.current) return;
      const map = L.map(container.current, {
        zoomControl: true,
        scrollWheelZoom: true,
      }).setView([21.4, 78.2], 5);
      mapRef.current = map;
      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(map);

      fetch(`${API_BASE_URL}/api/map/geojson`)
        .then((response) => {
          if (!response.ok) throw new Error(`Map API returned ${response.status}`);
          return response.json();
        })
        .then((payload) => {
          const features = Array.isArray(payload?.features) ? payload.features : [];
          const points: MapPoint[] = features
            .map((feature: any) => toMapPoint(feature))
            .filter((feature: MapPoint | null): feature is MapPoint => Boolean(feature));

          points.forEach((p: MapPoint) => {
            const marker = L.circleMarker([p.lat, p.lng], {
              radius: audience === "official" ? 9 : 8,
              color: "#fff",
              weight: 2,
              fillColor: riskColor[p.risk],
              fillOpacity: 0.92,
            });
            const barrierSummary = p.barriers.length
              ? p.barriers.slice(0, 2).map((barrier) => `${barrier.title} (${barrier.severity})`).join(" · ")
              : "No project-specific barriers recorded";
            const official = `<button type="button" class="map-popup popup-project-link" data-project-id="${p.id}"><span class="popup-risk ${p.risk.toLowerCase()}">${p.risk} RISK · ${p.probability}%</span><strong>${p.name}</strong><small>${p.district} · ${p.stage}</small><div><b>Compensation</b><span>${p.compensation}%</span></div><p>${barrierSummary}</p><span class="popup-cta">Open risk analysis →</span></button>`;
            const civilian = `<button type="button" class="map-popup civilian-popup popup-project-link" data-project-id="${p.id}"><span class="popup-status">PUBLIC PROJECT STATUS</span><strong>${p.name}</strong><small>${p.district} · Current stage: ${p.stage}</small><p>${p.status}</p><span class="popup-cta">View project details →</span></button>`;
            marker
              .bindPopup(audience === "official" ? official : civilian, {
                maxWidth: 270,
              })
              .addTo(map);
          });

          if (points.length > 0) {
            const bounds = L.latLngBounds(points.map((point: MapPoint) => [point.lat, point.lng]));
            map.fitBounds(bounds.pad(0.2));
          }
        })
        .catch((error) => {
          console.warn("Unable to load project map data:", error);
        })
        .finally(() => {
          setTimeout(() => map.invalidateSize(), 80);
        });
    });

    return () => {
      disposed = true;
      mapContainer.removeEventListener("click", openProject);
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, [audience]);

  return (
    <div
      ref={container}
      className={`leaflet-project-map ${audience}`}
      aria-label={`${audience} project map`}
    />
  );
}
