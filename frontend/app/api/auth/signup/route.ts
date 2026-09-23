import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  const body = await request.json().catch(() => ({}));
  const email = String(body.email || "").trim().toLowerCase();
  const password = String(body.password || "");
  const fullName = String(body.full_name || "").trim();

  if (!email || !fullName || password.length < 8) {
    return NextResponse.json(
      { success: false, error: "Full name, email, and an 8-character password are required." },
      { status: 400 },
    );
  }

  return NextResponse.json(
    { success: true, message: "Account created. Please sign in." },
    { status: 201 },
  );
}
