import { betterAuth } from "better-auth";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "your-super-secret-key-change-in-production",
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL || "",
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // For simplicity in this implementation
  },
  socialProviders: {
    // No third-party providers as per requirements
  },
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
    cookie: {
      secure: process.env.NODE_ENV === "production",
      httpOnly: true,
      maxAge: 7 * 24 * 60 * 60, // 7 days
    },
  },
});