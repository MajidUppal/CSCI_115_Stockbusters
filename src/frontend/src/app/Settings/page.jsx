"use client";

import { useState } from "react";
import { User, Shield, Bell, Globe, Trash2 } from "lucide-react";
import SettingsSection from "@/components/Settings/SettingsSection";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";

export default function Settings() {
  const [profile, setProfile] = useState({
    fullName: "John Doe",
    email: "john.doe@example.com",
    phone: "+1 (555) 123-4567",
  });

  const [investmentProfile, setInvestmentProfile] = useState({
    riskTolerance: "moderate",
    investmentGoal: "growth",
    timeHorizon: "5-10",
  });

  const [preferences, setPreferences] = useState({
    language: "en",
    currency: "USD",
    notifications: true,
  });

  return (
    <div className="min-h-screen bg-background py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-foreground">Settings & Preferences</h1>

        {/* Personal Information */}
        <SettingsSection title="Personal Information" icon={User}>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="fullName" className="text-foreground font-medium">
                Full Name
              </Label>
              <Input
                id="fullName"
                value={profile.fullName}
                onChange={(e) => setProfile({ ...profile, fullName: e.target.value })}
                className="bg-background border-input text-foreground placeholder:text-muted-foreground focus-visible:ring-2 focus-visible:ring-ring"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email" className="text-foreground font-medium">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                value={profile.email}
                onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                className="bg-background border-input text-foreground placeholder:text-muted-foreground focus-visible:ring-2 focus-visible:ring-ring"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone" className="text-foreground font-medium">
                Phone Number
              </Label>
              <Input
                id="phone"
                type="tel"
                value={profile.phone}
                onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                className="bg-background border-input text-foreground placeholder:text-muted-foreground focus-visible:ring-2 focus-visible:ring-ring"
              />
            </div>
            <Button className="mt-4">Save Changes</Button>
          </div>
        </SettingsSection>

        {/* Investment Profile */}
        <SettingsSection title="Investment Profile" icon={Globe}>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="riskTolerance" className="text-foreground font-medium">
                Risk Tolerance
              </Label>
              <Select
                value={investmentProfile.riskTolerance}
                onValueChange={(value) =>
                  setInvestmentProfile({ ...investmentProfile, riskTolerance: value })
                }
              >
                <SelectTrigger className="bg-background border-input text-foreground focus:ring-2 focus:ring-ring">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-popover border-border">
                  <SelectItem value="conservative" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    Conservative
                  </SelectItem>
                  <SelectItem value="moderate" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    Moderate
                  </SelectItem>
                  <SelectItem value="aggressive" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    Aggressive
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="investmentGoal" className="text-foreground font-medium">
                Investment Goal
              </Label>
              <Select
                value={investmentProfile.investmentGoal}
                onValueChange={(value) =>
                  setInvestmentProfile({ ...investmentProfile, investmentGoal: value })
                }
              >
                <SelectTrigger className="bg-background border-input text-foreground focus:ring-2 focus:ring-ring">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-popover border-border">
                  <SelectItem value="income" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    Income
                  </SelectItem>
                  <SelectItem value="growth" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    Growth
                  </SelectItem>
                  <SelectItem value="balanced" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    Balanced
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="timeHorizon" className="text-foreground font-medium">
                Time Horizon
              </Label>
              <Select
                value={investmentProfile.timeHorizon}
                onValueChange={(value) =>
                  setInvestmentProfile({ ...investmentProfile, timeHorizon: value })
                }
              >
                <SelectTrigger className="bg-background border-input text-foreground focus:ring-2 focus:ring-ring">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-popover border-border">
                  <SelectItem value="0-2" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    0-2 years
                  </SelectItem>
                  <SelectItem value="3-5" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    3-5 years
                  </SelectItem>
                  <SelectItem value="5-10" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    5-10 years
                  </SelectItem>
                  <SelectItem value="10+" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    10+ years
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button className="mt-4">Update Profile</Button>
          </div>
        </SettingsSection>

        {/* Preferences */}
        <SettingsSection title="Preferences" icon={Bell}>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="language" className="text-foreground font-medium">
                Language
              </Label>
              <Select
                value={preferences.language}
                onValueChange={(value) => setPreferences({ ...preferences, language: value })}
              >
                <SelectTrigger className="bg-background border-input text-foreground focus:ring-2 focus:ring-ring">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-popover border-border">
                  <SelectItem value="en" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    English
                  </SelectItem>
                  <SelectItem value="es" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    Spanish
                  </SelectItem>
                  <SelectItem value="fr" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    French
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="currency" className="text-foreground font-medium">
                Currency
              </Label>
              <Select
                value={preferences.currency}
                onValueChange={(value) => setPreferences({ ...preferences, currency: value })}
              >
                <SelectTrigger className="bg-background border-input text-foreground focus:ring-2 focus:ring-ring">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-popover border-border">
                  <SelectItem value="USD" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    USD ($)
                  </SelectItem>
                  <SelectItem value="EUR" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    EUR (€)
                  </SelectItem>
                  <SelectItem value="GBP" className="text-popover-foreground hover:bg-accent focus:bg-accent">
                    GBP (£)
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center justify-between py-2">
              <div className="space-y-0.5">
                <Label htmlFor="notifications" className="text-foreground font-medium">
                  Email Notifications
                </Label>
                <p className="text-sm text-muted-foreground">
                  Receive email updates about your portfolio
                </p>
              </div>
              <Switch
                id="notifications"
                checked={preferences.notifications}
                onCheckedChange={(checked) =>
                  setPreferences({ ...preferences, notifications: checked })
                }
              />
            </div>
          </div>
        </SettingsSection>

        {/* Security */}
        <SettingsSection title="Security" icon={Shield}>
          <div className="space-y-3">
            <Button variant="outline" className="w-full">
              Change Password
            </Button>
            <Button variant="outline" className="w-full">
              View Login Activity
            </Button>
          </div>
        </SettingsSection>

        {/* Danger Zone */}
        <SettingsSection title="Danger Zone" icon={Trash2}>
          <div className="space-y-3">
            <p className="text-sm text-muted-foreground mb-4">
              Irreversible actions that will affect your account
            </p>
            <Button variant="outline" className="w-full">
              Logout
            </Button>
            <Button variant="destructive" className="w-full">
              Delete Account
            </Button>
          </div>
        </SettingsSection>
      </div>
    </div>
  );
}
