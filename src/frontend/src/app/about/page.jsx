"use client";
import AboutSection from "@/components/about/AboutSection";
import { Card, CardContent } from "@/components/ui/card";
import Image from "next/image";

const teamMembers = [
  {
    name: "Mahmood Masqati",
    role: "Frontend Developer & UX Designer & Cloud Deployment Engineer",
    image: "/assets/team/mahmood.jpg",
    fallback: "MM",
    color: "from-blue-500 to-cyan-500"
  },
  {
    name: "Majid Uppal",
    role: "Backend Developer & Gen AI Engineer",
    image: "/assets/team/majid.jpg",
    fallback: "MU",
    color: "from-purple-500 to-pink-500"
  },
  {
    name: "Seraphim Eilken",
    role: "RAG Specialist & CI/CD Engineer",
    image: "/assets/team/seraphim.jpg",
    fallback: "SE",
    color: "from-green-500 to-emerald-500"
  },
  {
    name: "Sirisom Pranivong",
    role: "Quantimental Model Developer & Data Engineer",
    image: "/assets/team/sirisom.jpg",
    fallback: "SP",
    color: "from-orange-500 to-red-500"
  }
];

export default function Page() {
  return (
    <div className="min-h-screen w-full bg-background p-8 flex flex-col items-center">
      <h1 className="text-4xl font-extrabold mb-12 text-center text-foreground">
        About Stock Busters
      </h1>

      {/* Team Section */}
      <div className="w-full max-w-6xl mx-auto mt-16 mb-10">
        <div className="text-center mb-12">
          <div className="inline-block mb-4">
            <div className="h-1 w-20 bg-gradient-to-r from-red-500 via-yellow-500 via-green-500 via-cyan-500 to-blue-500 rounded-full mx-auto" />
          </div>
          <h2 className="text-4xl font-bold mb-4 text-foreground">Meet the Team</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            A dedicated group of developers and data scientists passionate about 
            financial technology and AI innovation.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {teamMembers.map((member, index) => (
            <Card 
              key={index} 
              className="group hover:shadow-xl transition-all duration-300 border-border hover:border-primary/50"
            >
              <CardContent className="p-6">
                <div className="flex flex-col items-center text-center">
                  <div className="relative w-32 h-32 mb-4 rounded-full overflow-hidden border-4 border-primary/20 group-hover:border-primary/50 transition-all">
                    <Image
                      src={member.image}
                      alt={member.name}
                      fill
                      className="object-cover"
                      onError={(e) => {
                        // Fallback to gradient with initials if image fails
                        e.target.style.display = 'none';
                      }}
                    />
                    {/* Fallback gradient background */}
                    <div className={`absolute inset-0 bg-gradient-to-br ${member.color} flex items-center justify-center -z-10`}>
                      <span className="text-4xl font-bold text-white">
                        {member.fallback}
                      </span>
                    </div>
                  </div>
                  <h3 className="text-xl font-bold text-primary mb-1">
                    {member.name}
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    {member.role}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
      <AboutSection title="Our Mission">
        Stock Busters exists to empower retail investors by cutting through market noise
        and delivering clean, actionable insights.
      </AboutSection>

      <AboutSection title="The Problem We Solve">
        Most retail investors face information overload and analysis paralysis.
      </AboutSection>

      <AboutSection title="Our Solution">
        Stock Busters uses AI to simplify market research and generate actionable insights.
      </AboutSection>

      <AboutSection title="Why We Built Stock Busters">
        Retail investors deserve institutional-grade clarity and strategy.
      </AboutSection>
    </div>
  );
}