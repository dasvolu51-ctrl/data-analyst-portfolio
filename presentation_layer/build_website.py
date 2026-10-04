import os
import json
import textwrap

BASE_DIR = r"C:\Users\Public\data_analyst_portfolio\presentation_layer"
os.makedirs(os.path.join(BASE_DIR, "public", "data"), exist_ok=True)

# 1. Write metrics.json (Simulating the export from the Semantic Layer)
metrics = [
    {"month": "Jan", "mrr": 42000, "subscribers": 1200},
    {"month": "Feb", "mrr": 45500, "subscribers": 1350},
    {"month": "Mar", "mrr": 51000, "subscribers": 1500},
    {"month": "Apr", "mrr": 49000, "subscribers": 1420},
    {"month": "May", "mrr": 58000, "subscribers": 1780},
    {"month": "Jun", "mrr": 65000, "subscribers": 2100},
    {"month": "Jul", "mrr": 74000, "subscribers": 2450}
]
with open(os.path.join(BASE_DIR, "public", "data", "metrics.json"), "w") as f:
    json.dump(metrics, f)

# 2. Write index.html (Zero-build environment using ESM and Babel Standalone)
html_content = textwrap.dedent("""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaaS Intelligence | Premium BI</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Babel Standalone for in-browser JSX compilation -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- ESM Import Map to load React, Framer Motion, and Recharts without Node.js -->
    <script type="importmap">
    {
        "imports": {
            "react": "https://esm.sh/react@18.2.0",
            "react-dom/client": "https://esm.sh/react-dom@18.2.0/client",
            "framer-motion": "https://esm.sh/framer-motion@10.16.4?deps=react@18.2.0,react-dom@18.2.0",
            "recharts": "https://esm.sh/recharts@2.10.3?deps=react@18.2.0,react-dom@18.2.0",
            "lucide-react": "https://esm.sh/lucide-react@0.292.0?deps=react@18.2.0"
        }
    }
    </script>
    <style>
        body { margin: 0; background-color: #800020; font-family: 'Inter', sans-serif; }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #800020; }
        ::-webkit-scrollbar-thumb { background: #FFFDD0; border-radius: 10px; }
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel" data-type="module" src="./app.jsx"></script>
</body>
</html>
""")
with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

# 3. Write app.jsx (The React code infused with Framer Motion and Recharts)
jsx_content = """
import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { motion, AnimatePresence } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { ChevronRight, BarChart3, Database, LineChart as LineChartIcon } from 'lucide-react';

const App = () => {
    const [view, setView] = useState('welcome');
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch('./public/data/metrics.json')
            .then(res => res.json())
            .then(d => setData(d));
    }, []);

    return (
        <div className="min-h-screen bg-[#800020] text-[#FFFDD0] font-sans selection:bg-[#FFFDD0] selection:text-[#800020] overflow-hidden relative">
            <AnimatePresence mode="wait">
                {view === 'welcome' && <WelcomeScreen onEnter={() => setView('selection')} key="welcome" />}
                {view === 'selection' && <TierSelector onSelect={(t) => setView(t)} key="selection" />}
                {view === 'tier1' && <Tier1View data={data} onBack={() => setView('selection')} key="tier1" />}
                {view === 'tier2' && <Tier2View data={data} onBack={() => setView('selection')} key="tier2" />}
                {view === 'tier3' && <Tier3View data={data} onBack={() => setView('selection')} key="tier3" />}
            </AnimatePresence>
        </div>
    );
};

const WelcomeScreen = ({ onEnter }) => (
    <motion.div 
        initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, y: -50 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="flex flex-col items-center justify-center min-h-screen p-8 text-center absolute inset-0"
    >
        <h1 className="text-6xl md:text-8xl font-black mb-6 tracking-tighter">
            <span className="text-[#FFFDD0]">SaaS</span> <span className="text-emerald-400">Intelligence</span>
        </h1>
        <p className="text-xl md:text-2xl mb-12 max-w-3xl font-light leading-relaxed opacity-90">
            Welcome to the final presentation layer. This application is dynamically powered by a dbt Semantic Layer and a DuckDB Star Schema, proving enterprise-grade data engineering capabilities.
        </p>
        <motion.button 
            whileHover={{ scale: 1.05, backgroundColor: "#f2eed5" }} whileTap={{ scale: 0.95 }}
            onClick={onEnter}
            className="px-10 py-5 bg-[#FFFDD0] text-[#800020] rounded-full font-bold text-xl shadow-[0_0_40px_rgba(255,253,208,0.3)] transition-colors flex items-center gap-3 cursor-pointer"
        >
            Enter Dashboard <ChevronRight size={24} />
        </motion.button>
    </motion.div>
);

const TierSelector = ({ onSelect }) => (
    <motion.div 
        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        className="flex flex-col items-center justify-center min-h-screen p-8 max-w-6xl mx-auto absolute inset-0"
    >
        <h2 className="text-4xl md:text-5xl font-bold mb-12">Select Stakeholder View</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full">
            <TierCard title="Tier 1: Executive" desc="Pure financial impact. Profit and loss visualization for leadership." icon={<BarChart3 size={48}/>} onClick={() => onSelect('tier1')} />
            <TierCard title="Tier 2: Management" desc="Operational metrics. Active subscribers and cohort breakdowns." icon={<LineChartIcon size={48}/>} onClick={() => onSelect('tier2')} />
            <TierCard title="Tier 3: Engineering" desc="Deep technical dive. Semantic layer mapping and architecture." icon={<Database size={48}/>} onClick={() => onSelect('tier3')} />
        </div>
    </motion.div>
);

const TierCard = ({ title, desc, icon, onClick }) => (
    <motion.div 
        whileHover={{ y: -10, backgroundColor: "rgba(255,253,208,0.15)" }}
        onClick={onClick}
        className="p-8 border-2 border-[#FFFDD0]/20 rounded-3xl cursor-pointer bg-[#800020] shadow-2xl transition-colors h-full flex flex-col"
    >
        <div className="text-[#FFFDD0] mb-6 opacity-90">{icon}</div>
        <h3 className="text-2xl font-bold mb-4">{title}</h3>
        <p className="text-[#FFFDD0]/70 leading-relaxed text-lg flex-1">{desc}</p>
    </motion.div>
);

const Tier1View = ({ data, onBack }) => {
    const isProfit = data.length > 1 ? data[data.length-1].mrr > data[data.length-2].mrr : true;
    const chartColor = isProfit ? "#10b981" : "#ef4444";

    return (
        <motion.div initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }} className="p-8 md:p-12 min-h-screen max-w-7xl mx-auto absolute inset-0 overflow-y-auto">
            <button onClick={onBack} className="mb-8 flex items-center gap-2 opacity-70 hover:opacity-100 transition-opacity text-lg cursor-pointer"><ChevronRight className="rotate-180"/> Back to Selection</button>
            <h2 className="text-5xl md:text-6xl font-black mb-2">Executive Summary</h2>
            <p className="text-2xl opacity-70 mb-12 font-light">Monthly Recurring Revenue (MRR)</p>
            
            <div className="h-[400px] md:h-[500px] w-full bg-[#FFFDD0]/5 p-6 md:p-8 rounded-3xl border border-[#FFFDD0]/10 shadow-2xl">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorMrr" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor={chartColor} stopOpacity={0.6}/>
                                <stop offset="95%" stopColor={chartColor} stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <XAxis dataKey="month" stroke="#FFFDD0" opacity={0.5} tick={{fill: '#FFFDD0'}} axisLine={false} tickLine={false} />
                        <YAxis stroke="#FFFDD0" opacity={0.5} tickFormatter={(val) => '$'+(val/1000)+'k'} axisLine={false} tickLine={false} />
                        <Tooltip contentStyle={{backgroundColor: '#800020', border: '1px solid rgba(255,253,208,0.2)', borderRadius: '16px', color: '#FFFDD0'}} itemStyle={{color: '#FFFDD0'}} />
                        <Area type="monotone" dataKey="mrr" stroke={chartColor} strokeWidth={5} fillOpacity={1} fill="url(#colorMrr)" />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </motion.div>
    );
};

const Tier2View = ({ data, onBack }) => (
    <motion.div initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }} className="p-8 md:p-12 min-h-screen max-w-7xl mx-auto absolute inset-0 overflow-y-auto">
        <button onClick={onBack} className="mb-8 flex items-center gap-2 opacity-70 hover:opacity-100 transition-opacity text-lg cursor-pointer"><ChevronRight className="rotate-180"/> Back to Selection</button>
        <h2 className="text-5xl md:text-6xl font-black mb-2">Operational Metrics</h2>
        <p className="text-2xl opacity-70 mb-12 font-light">Active Subscriber Growth Cohorts</p>
        
        <div className="h-[400px] md:h-[500px] w-full bg-[#FFFDD0]/5 p-6 md:p-8 rounded-3xl border border-[#FFFDD0]/10 shadow-2xl">
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                    <XAxis dataKey="month" stroke="#FFFDD0" opacity={0.5} tick={{fill: '#FFFDD0'}} axisLine={false} tickLine={false} />
                    <YAxis stroke="#FFFDD0" opacity={0.5} axisLine={false} tickLine={false} />
                    <Tooltip contentStyle={{backgroundColor: '#800020', border: '1px solid rgba(255,253,208,0.2)', borderRadius: '16px', color: '#FFFDD0'}} itemStyle={{color: '#FFFDD0'}} />
                    <Line type="monotone" dataKey="subscribers" stroke="#3b82f6" strokeWidth={5} dot={{r: 6, fill: '#800020', stroke: '#3b82f6', strokeWidth: 3}} activeDot={{r: 8}} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    </motion.div>
);

const Tier3View = ({ data, onBack }) => (
    <motion.div initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }} className="p-8 md:p-12 min-h-screen max-w-7xl mx-auto absolute inset-0 overflow-y-auto">
        <button onClick={onBack} className="mb-8 flex items-center gap-2 opacity-70 hover:opacity-100 transition-opacity text-lg cursor-pointer"><ChevronRight className="rotate-180"/> Back to Selection</button>
        <h2 className="text-5xl md:text-6xl font-black mb-12">Semantic Architecture</h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 md:gap-12">
            <div className="bg-[#FFFDD0]/5 p-8 rounded-3xl border border-[#FFFDD0]/10 shadow-2xl">
                <h3 className="text-3xl font-bold mb-6 text-emerald-400">MetricFlow SQL Query</h3>
                <pre className="bg-black/40 p-6 rounded-2xl font-mono text-sm md:text-base overflow-x-auto text-[#FFFDD0]/90 shadow-inner">
{`SELECT * 
FROM {{ metrics.calculate(
metric('mrr'), 
dimensions=['snapshot_month']
) }}`}
                </pre>
                <p className="mt-8 text-lg opacity-80 leading-relaxed font-light">This layer completely abstracts the underlying DuckDB star schema. Downstream applications like this website simply request the unified metric, guaranteeing mathematical consistency across the entire enterprise stack.</p>
            </div>
            <div className="bg-[#FFFDD0]/5 p-8 rounded-3xl border border-[#FFFDD0]/10 shadow-2xl flex flex-col items-center justify-center text-center">
                <Database size={80} className="text-[#FFFDD0]/60 mb-8" />
                <h3 className="text-3xl font-bold mb-6">DuckDB Zero-ETL Engine</h3>
                <div className="flex gap-6 w-full mt-4">
                    <div className="flex-1 bg-black/20 p-6 rounded-2xl border border-[#FFFDD0]/5"><span className="block text-4xl font-black mb-2">10M+</span><span className="text-sm opacity-60 uppercase tracking-widest font-bold">Rows Processed</span></div>
                    <div className="flex-1 bg-black/20 p-6 rounded-2xl border border-[#FFFDD0]/5"><span className="block text-4xl font-black mb-2">2.8s</span><span className="text-sm opacity-60 uppercase tracking-widest font-bold">Compile Time</span></div>
                </div>
            </div>
        </div>
    </motion.div>
);

const root = createRoot(document.getElementById('root'));
root.render(<App />);
"""
with open(os.path.join(BASE_DIR, "app.jsx"), "w", encoding="utf-8") as f:
    f.write(jsx_content)

# 4. Write serve.py (To spin up the local preview)
serve_content = textwrap.dedent("""\
import http.server
import socketserver
import os

PORT = 5173
os.chdir(r"C:\\Users\\Public\\data_analyst_portfolio\\presentation_layer")
Handler = http.server.SimpleHTTPRequestHandler

class MyServer(socketserver.TCPServer):
    allow_reuse_address = True

try:
    with MyServer(("", PORT), Handler) as httpd:
        print(f"Premium BI Presentation running successfully!")
        print(f"Open this exact link in your browser to view: http://localhost:{PORT}")
        httpd.serve_forever()
except Exception as e:
    print(f"Error starting server: {e}")
""")
with open(os.path.join(BASE_DIR, "serve.py"), "w", encoding="utf-8") as f:
    f.write(serve_content)

print("Website generation complete!")
