import { NextRequest, NextResponse } from "next/server";

const officialAccounts: Record<string, string> = {
  "umang.gov@officials.in": "Official@123",
  "admin.gov@officials.in": "Admin@123",
  "officer.gov@officials.in": "Officer@123",
  "director.gov@officials.in": "Director@123",
};

export async function POST(request: NextRequest) {
  const body = await request.json().catch(() => ({}));
  const email = String(body.email || "").trim().toLowerCase();
  const password = String(body.password || "");
  const role = String(body.role || "civilian").toLowerCase();

  const valid =
    role === "official"
      ? officialAccounts[email] === password
      : Boolean(email && password.length >= 8);

  if (!valid) {
    return NextResponse.json(
      { success: false, error: "Invalid email or password." },
      { status: 401 },
    );
  }

  return NextResponse.json({
    success: true,
    token: crypto.randomUUID(),
    user: { email, role, full_name: email.split("@")[0] },
  });
}
