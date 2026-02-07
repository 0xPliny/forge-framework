import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { ArrowRight, Terminal, Cpu, Shield, Zap, GitBranch, Database, Layers } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col overflow-x-hidden">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 border-b border-white/5 bg-[#0a0e1a]/80 backdrop-blur-md">
        <div className="container mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img src="/assets/forge-logo-lava.webp" alt="FORGE" className="w-8 h-8" />
            <span className="font-display font-bold text-xl tracking-widest text-white">FORGE</span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-mono text-slate-400">
            <a href="#methodology" className="hover:text-orange-500 transition-colors">METHODOLOGY</a>
            <a href="#impact" className="hover:text-orange-500 transition-colors">IMPACT</a>
            <a href="#tools" className="hover:text-orange-500 transition-colors">TOOLS</a>
            <Button variant="outline" className="border-orange-500/50 text-orange-500 hover:bg-orange-500/10 font-mono rounded-none">
              GITHUB
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center pt-20">
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#0a0e1a]/80 to-[#0a0e1a]" />
        </div>
        
        <div className="container mx-auto px-6 relative z-10 grid lg:grid-cols-2 gap-12 items-center">
          <motion.div 
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 border border-orange-500/30 bg-orange-500/5 text-orange-500 text-xs font-mono tracking-wider">
              <span className="w-2 h-2 bg-orange-500 rounded-full animate-pulse" />
              ENTERPRISE GRADE
            </div>
            
            <h1 className="font-display text-5xl md:text-7xl font-bold leading-tight text-white">
              ORCHESTRATED <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-600 text-glow">
                INTELLIGENCE
              </span>
            </h1>
            
            <p className="text-slate-400 text-lg md:text-xl max-w-xl leading-relaxed">
              Framework for Orchestrated, Repeatable, Governed Engineering. 
              Turn raw AI capability into reliable, production-grade engineering output.
            </p>
            
            <div className="flex flex-wrap gap-4">
              <Button className="h-12 px-8 bg-orange-600 hover:bg-orange-500 text-white font-bold rounded-none tracking-wide">
                GET STARTED
              </Button>
              <Button variant="outline" className="h-12 px-8 border-slate-700 text-slate-300 hover:border-orange-500/50 hover:text-orange-500 rounded-none font-mono">
                VIEW DOCUMENTATION
              </Button>
            </div>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, delay: 0.2 }}
            className="relative hidden lg:block"
          >
            <div className="relative w-full aspect-square max-w-lg mx-auto animate-float">
              <img src="/assets/hero-bg-lava.webp" alt="The Forge" className="w-full h-full object-contain drop-shadow-[0_0_50px_rgba(255,100,0,0.2)]" />
              
              {/* Floating UI Elements */}
              <div className="absolute -top-10 -right-10 p-4 bg-[#0a0e1a]/90 border border-orange-500/30 backdrop-blur-md">
                <div className="flex items-center gap-3 mb-2">
                  <Terminal className="w-4 h-4 text-orange-500" />
                  <span className="text-xs font-mono text-orange-500">SYSTEM_METRICS</span>
                </div>
                <div className="space-y-1 font-mono text-xs text-slate-400">
                  <div className="flex justify-between gap-8"><span>CORE</span><span className="text-orange-400">ONLINE</span></div>
                  <div className="flex justify-between gap-8"><span>GOVERNANCE</span><span className="text-orange-400">ACTIVE</span></div>
                  <div className="flex justify-between gap-8"><span>MEMORY</span><span className="text-orange-400">SYNCED</span></div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Methodology Section */}
      <section id="methodology" className="py-32 relative">
        <div className="container mx-auto px-6">
          <div className="text-center mb-20">
            <h2 className="font-display text-4xl font-bold text-white mb-4">CORE PROTOCOLS</h2>
            <p className="text-slate-400 max-w-2xl mx-auto">
              Structured workflows that replace ad-hoc prompting with engineering rigor.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                title: "R-I-S-E",
                subtitle: "Creation & Design",
                desc: "Research → Implement → Synthesize → Execute. The standard protocol for generating new capabilities.",
                icon: "/assets/rise-icon.webp"
              },
              {
                title: "C-A-R-E",
                subtitle: "Debugging & Optimization",
                desc: "Collect → Analyze → Refine → Execute. A systematic loop for resolving defects and optimizing performance.",
                icon: "/assets/care-icon.webp"
              },
              {
                title: "HARVEST",
                subtitle: "Knowledge Extraction",
                desc: "7-phase pipeline for converting raw code into structured, semantic documentation.",
                icon: "/assets/harvest-icon.webp"
              }
            ].map((item, i) => (
              <motion.div 
                key={i}
                whileHover={{ y: -10 }}
                className="cyber-border p-8 group border border-white/5 hover:border-orange-500/30 transition-colors bg-white/5"
              >
                <div className="mb-6 relative">
                  <div className="absolute inset-0 bg-orange-500/20 blur-xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity" />
                  <img src={item.icon} alt={item.title} className="w-16 h-16 relative z-10" />
                </div>
                <h3 className="font-display text-2xl font-bold text-white mb-2 group-hover:text-orange-500 transition-colors">
                  {item.title}
                </h3>
                <p className="font-mono text-xs text-orange-500 mb-4 tracking-wider uppercase">{item.subtitle}</p>
                <p className="text-slate-400 leading-relaxed">
                  {item.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Impact Section */}
      <section id="impact" className="py-32 bg-[#0f1422]/50 border-y border-white/5">
        <div className="container mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center">
          <div>
            <h2 className="font-display text-4xl font-bold text-white mb-8">
              MEASURABLE <span className="text-orange-500">IMPACT</span>
            </h2>
            
            <div className="space-y-8">
              {[
                { label: "Cost Efficiency", value: "21x", desc: "Reduced cost per unit from $7.64 to $0.35" },
                { label: "Development Velocity", value: "10x", desc: "Increase in output while reducing error rates" },
                { label: "Knowledge Growth", value: "+396%", desc: "Expansion of structured documentation base" }
              ].map((stat, i) => (
                <div key={i} className="border-l-2 border-orange-500/30 pl-6 py-2">
                  <div className="font-display text-5xl font-bold text-white mb-1">{stat.value}</div>
                  <div className="font-mono text-orange-500 text-sm mb-2">{stat.label}</div>
                  <p className="text-slate-400 text-sm">{stat.desc}</p>
                </div>
              ))}
            </div>
          </div>
          
          <div className="relative">
            <div className="absolute inset-0 bg-orange-500/10 blur-3xl rounded-full" />
            <img src="/assets/impact-chart.webp" alt="Impact Chart" className="relative z-10 w-full border border-orange-500/20 bg-[#0a0e1a]/80 backdrop-blur-sm" />
          </div>
        </div>
      </section>

      {/* Tools Section */}
      <section id="tools" className="py-32">
        <div className="container mx-auto px-6">
          <div className="text-center mb-20">
            <h2 className="font-display text-4xl font-bold text-white mb-4">TECHNOLOGY STACK</h2>
            <p className="text-slate-400">Powered by a modern stack of specialized tools.</p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { name: "Python", icon: <Terminal /> },
              { name: "TypeScript", icon: <Cpu /> },
              { name: "Docker", icon: <Layers /> },
              { name: "FastAPI", icon: <Zap /> },
              { name: "PostgreSQL", icon: <Database /> },
              { name: "Git", icon: <GitBranch /> },
              { name: "OpenAI", icon: <Cpu /> },
              { name: "Anthropic", icon: <Shield /> }
            ].map((tool, i) => (
              <div key={i} className="p-6 border border-white/5 bg-white/5 hover:bg-orange-500/10 hover:border-orange-500/30 transition-all flex flex-col items-center gap-3 group">
                <div className="text-slate-400 group-hover:text-orange-500 transition-colors">
                  {tool.icon}
                </div>
                <span className="font-mono text-sm text-slate-300">{tool.name}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-white/5 bg-[#05070d]">
        <div className="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-3">
            <img src="/assets/forge-logo-lava.webp" alt="FORGE" className="w-6 h-6 grayscale opacity-50" />
            <span className="font-display font-bold text-slate-500">FORGE FRAMEWORK</span>
          </div>
          <div className="text-slate-600 text-sm font-mono">
            © 2026 Chase Logan. Empowering AI Engineering.
          </div>
        </div>
      </footer>
    </div>
  );
}
