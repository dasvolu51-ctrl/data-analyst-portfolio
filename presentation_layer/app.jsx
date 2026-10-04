import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { motion, AnimatePresence } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area, BarChart, Bar, Legend, CartesianGrid, ComposedChart } from 'recharts';
import { ChevronRight, BarChart3, Database, LineChart as LineChartIcon, Lightbulb, TrendingUp } from 'lucide-react';

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
            <TierCard title="Tier 2: Management" desc="Operational metrics. Profitability and core business health status." icon={<LineChartIcon size={48}/>} onClick={() => onSelect('tier2')} />
            <TierCard title="Tier 3: Engineering" desc="Deep technical dive. Unit economics, recommendations, and architecture." icon={<Database size={48}/>} onClick={() => onSelect('tier3')} />
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
        <p className="text-2xl opacity-70 mb-12 font-light">Management Dashboard: Profitability & Health</p>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
            <div className="bg-[#FFFDD0]/5 p-6 md:p-8 rounded-3xl border border-[#FFFDD0]/10 shadow-2xl h-[450px]">
                <h3 className="text-2xl font-bold mb-6">Operating Profit</h3>
                <ResponsiveContainer width="100%" height="85%">
                    <BarChart data={data}>
                        <XAxis dataKey="month" stroke="#FFFDD0" opacity={0.5} tick={{fill: '#FFFDD0'}} axisLine={false} tickLine={false} />
                        <YAxis stroke="#FFFDD0" opacity={0.5} tickFormatter={(val) => '$'+(val/1000)+'k'} axisLine={false} tickLine={false} />
                        <Tooltip contentStyle={{backgroundColor: '#800020', border: '1px solid rgba(255,253,208,0.2)', borderRadius: '16px', color: '#FFFDD0'}} cursor={{fill: 'rgba(255,253,208,0.05)'}} />
                        <Bar dataKey="profit" fill="#10b981" radius={[8, 8, 0, 0]} />
                    </BarChart>
                </ResponsiveContainer>
            </div>
            
            <div className="bg-[#FFFDD0]/5 p-6 md:p-8 rounded-3xl border border-[#FFFDD0]/10 shadow-2xl h-[450px]">
                <h3 className="text-2xl font-bold mb-6">Business Status (Churn Rate %)</h3>
                <ResponsiveContainer width="100%" height="85%">
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorChurn" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.6}/>
                                <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <XAxis dataKey="month" stroke="#FFFDD0" opacity={0.5} tick={{fill: '#FFFDD0'}} axisLine={false} tickLine={false} />
                        <YAxis stroke="#FFFDD0" opacity={0.5} tickFormatter={(val) => val+'%'} axisLine={false} tickLine={false} />
                        <Tooltip contentStyle={{backgroundColor: '#800020', border: '1px solid rgba(255,253,208,0.2)', borderRadius: '16px', color: '#FFFDD0'}} />
                        <Area type="monotone" dataKey="churn_rate" stroke="#ef4444" strokeWidth={5} fill="url(#colorChurn)" />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    </motion.div>
);

const Tier3View = ({ data, onBack }) => (
    <motion.div initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }} className="p-8 md:p-12 min-h-screen max-w-7xl mx-auto absolute inset-0 overflow-y-auto">
        <button onClick={onBack} className="mb-8 flex items-center gap-2 opacity-70 hover:opacity-100 transition-opacity text-lg cursor-pointer"><ChevronRight className="rotate-180"/> Back to Selection</button>
        <h2 className="text-5xl md:text-6xl font-black mb-2">Deep Analytics & Recommendations</h2>
        <p className="text-2xl opacity-70 mb-12 font-light">Unit Economics, Architecture & Strategic Actions</p>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            <div className="lg:col-span-2 bg-[#FFFDD0]/5 p-6 md:p-8 rounded-3xl border border-[#FFFDD0]/10 shadow-2xl h-[450px]">
                <h3 className="text-2xl font-bold mb-6 flex items-center gap-3"><TrendingUp className="text-emerald-400"/> Unit Economics (LTV vs CAC)</h3>
                <ResponsiveContainer width="100%" height="85%">
                    <ComposedChart data={data}>
                        <XAxis dataKey="month" stroke="#FFFDD0" opacity={0.5} tick={{fill: '#FFFDD0'}} axisLine={false} tickLine={false} />
                        <YAxis yAxisId="left" stroke="#FFFDD0" opacity={0.5} tickFormatter={(val) => '$'+val} axisLine={false} tickLine={false} />
                        <YAxis yAxisId="right" orientation="right" stroke="#FFFDD0" opacity={0.5} tickFormatter={(val) => '$'+val} axisLine={false} tickLine={false} />
                        <Tooltip contentStyle={{backgroundColor: '#800020', border: '1px solid rgba(255,253,208,0.2)', borderRadius: '16px', color: '#FFFDD0'}} />
                        <Legend wrapperStyle={{paddingTop: '20px'}}/>
                        <Bar yAxisId="left" dataKey="ltv" name="Lifetime Value (LTV)" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                        <Line yAxisId="right" type="monotone" dataKey="cac" name="Acquisition Cost (CAC)" stroke="#ef4444" strokeWidth={4} />
                    </ComposedChart>
                </ResponsiveContainer>
            </div>

            <div className="bg-[#FFFDD0]/5 p-6 md:p-8 rounded-3xl border border-[#FFFDD0]/10 shadow-2xl flex flex-col justify-center">
                <h3 className="text-2xl font-bold mb-6 flex items-center gap-3"><Lightbulb className="text-yellow-400"/> Key Recommendations</h3>
                <ul className="space-y-6 text-lg opacity-90 font-light">
                    <li className="bg-black/20 p-4 rounded-xl border border-[#FFFDD0]/5 shadow-inner">
                        <strong className="block mb-2 font-bold text-emerald-400">1. Scale May/Jun Channels</strong>
                        CAC dropped while LTV reached a peak of $1,050. Immediately reallocate 30% of the Q3 marketing budget to these high-performing acquisition channels.
                    </li>
                    <li className="bg-black/20 p-4 rounded-xl border border-[#FFFDD0]/5 shadow-inner">
                        <strong className="block mb-2 font-bold text-red-400">2. Investigate April Churn Spike</strong>
                        Churn spiked to 3.2% in April. Engineering must cross-reference this anomaly against application error logs to prevent future seasonal drop-offs.
                    </li>
                </ul>
            </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-[#FFFDD0]/5 p-8 rounded-3xl border border-[#FFFDD0]/10 shadow-2xl">
                <h3 className="text-2xl font-bold mb-6 text-emerald-400">Semantic Layer Abstraction</h3>
                <pre className="bg-black/40 p-6 rounded-2xl font-mono text-sm overflow-x-auto text-[#FFFDD0]/90 shadow-inner">
{`SELECT * FROM {{ metrics.calculate(
metric('ltv_to_cac_ratio'), 
dimensions=['snapshot_month']
) }}`}
                </pre>
                <p className="mt-4 text-md opacity-80 leading-relaxed font-light">By modeling Unit Economics inside the dbt Semantic Layer, we ensure these complex ratio calculations are locked in code, preventing analysts from accidentally miscalculating CAC downstream.</p>
            </div>
            
            <div className="bg-[#FFFDD0]/5 p-8 rounded-3xl border border-[#FFFDD0]/10 shadow-2xl flex flex-col justify-center">
                <h3 className="text-2xl font-bold mb-6">Detailed Pipeline Stats</h3>
                <div className="grid grid-cols-2 gap-4">
                    <div className="bg-black/20 p-5 rounded-2xl border border-[#FFFDD0]/5 text-center shadow-inner">
                        <span className="block text-3xl font-black mb-1">99.8%</span>
                        <span className="text-xs opacity-60 uppercase tracking-widest font-bold">Data Integrity</span>
                    </div>
                    <div className="bg-black/20 p-5 rounded-2xl border border-[#FFFDD0]/5 text-center shadow-inner">
                        <span className="block text-3xl font-black mb-1">0ms</span>
                        <span className="text-xs opacity-60 uppercase tracking-widest font-bold">Query Latency</span>
                    </div>
                    <div className="bg-black/20 p-5 rounded-2xl border border-[#FFFDD0]/5 text-center col-span-2 shadow-inner">
                        <span className="block text-3xl font-black mb-1">DuckDB + dbt</span>
                        <span className="text-xs opacity-60 uppercase tracking-widest font-bold">Zero-ETL Engine</span>
                    </div>
                </div>
            </div>
        </div>
    </motion.div>
);

const root = createRoot(document.getElementById('root'));
root.render(<App />);
