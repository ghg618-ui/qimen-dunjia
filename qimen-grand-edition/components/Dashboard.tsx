"use client";

import React, { useState } from 'react';
import { Compass, Database, Star, Settings, Clock, Share2, Plus, Calendar, Zap } from 'lucide-react';

export default function ZenDashboard({ user }: { user: any }) {
    const [matter, setMatter] = useState('');

    return (
        <div className="min-h-screen bg-[#FDFDFD] text-zinc-900 flex flex-col md:flex-row antialiased">
            {/* Sidebar - Apple Control Style */}
            <nav className="w-full md:w-24 bg-white border-b md:border-b-0 md:border-r border-zinc-100 flex md:flex-col items-center py-10 gap-10">
                <div className="w-12 h-12 bg-zinc-900 rounded-2xl flex items-center justify-center shadow-xl shadow-zinc-200">
                    <Compass className="w-6 h-6 text-white" />
                </div>
                <div className="flex md:flex-col gap-10 text-zinc-300">
                    <button className="text-zinc-900"><Compass className="w-7 h-7" /></button>
                    <button className="hover:text-zinc-900 transition-all"><Database className="w-7 h-7" /></button>
                    <button className="hover:text-zinc-900 transition-all"><Settings className="w-7 h-7" /></button>
                </div>
                <div className="md:mt-auto">
                    <div className="w-12 h-12 rounded-full border-2 border-zinc-50 p-1">
                        <div className="w-full h-full rounded-full bg-zinc-100 flex items-center justify-center font-bold text-xs text-zinc-400">
                            HG
                        </div>
                    </div>
                </div>
            </nav>

            {/* Main Content Area */}
            <main className="flex-grow p-6 md:p-12 space-y-12">
                <header className="flex flex-col md:flex-row justify-between items-end gap-6">
                    <div className="space-y-2">
                        <div className="flex items-center gap-3">
                            <h1 className="text-3xl font-bold tracking-tight text-zinc-900">推演流转</h1>
                            {user.isVip && <span className="vip-tag">VIP 尊享</span>}
                        </div>
                        <p className="text-zinc-400 font-light flex items-center gap-2">
                            <Calendar className="w-4 h-4" /> 2026年 2月 24日 · 阳遁八局 · 五不遇时
                        </p>
                    </div>
                    <div className="flex gap-4">
                        <button className="h-12 px-6 rounded-2xl bg-white border border-zinc-100 text-sm font-semibold text-zinc-600 hover:shadow-md transition-all flex items-center gap-2">
                            <Share2 className="w-4 h-4" /> 导出卡片
                        </button>
                        <button className="h-12 px-8 rounded-2xl bg-zinc-900 text-white font-semibold text-sm shadow-xl shadow-zinc-200 active:scale-95 transition-all flex items-center gap-2">
                            <Plus className="w-4 h-4" /> 保存当前
                        </button>
                    </div>
                </header>

                {/* Matter Input */}
                <section className="bg-white rounded-3xl p-2 border border-zinc-100 shadow-sm">
                    <input
                        type="text"
                        placeholder="点击于此，开启本次时空推演..."
                        className="w-full bg-transparent px-8 py-6 text-2xl font-semibold text-zinc-800 outline-none placeholder:font-light placeholder:text-zinc-200"
                        value={matter}
                        onChange={(e) => setMatter(e.target.value)}
                    />
                </section>

                {/* Grid System */}
                <div className="grid grid-cols-1 xl:grid-cols-3 gap-12">
                    {/* Chart Rendering Area */}
                    <div className="xl:col-span-2 zen-glass p-8 min-h-[600px] flex flex-col">
                        <div className="grid grid-cols-3 gap-4 flex-grow">
                            {[4, 9, 2, 3, 5, 7, 8, 1, 6].map(n => (
                                <div key={n} className="border border-zinc-50 rounded-2xl p-4 flex flex-col justify-between hover:bg-zinc-50/50 transition-colors cursor-pointer group relative">
                                    <div className="flex justify-between items-start">
                                        <span className="text-[10px] font-bold text-zinc-200 tracking-widest">{n == 5 ? 'ZHONG' : 'PALACE'}</span>
                                        <div className="w-1.5 h-1.5 rounded-full bg-zinc-100 group-hover:bg-amber-400 transition-colors" />
                                    </div>
                                    <div className="text-center font-light text-zinc-300 text-sm">
                                        宫位矩阵核心
                                    </div>
                                    <div className="flex justify-between items-end">
                                        <span className="text-xs text-zinc-100">---</span>
                                        <span className="text-2xl font-serif text-zinc-200">{n}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="mt-6 pt-6 border-t border-zinc-50 flex justify-center">
                            <p className="text-[10px] text-zinc-300 tracking-[0.2em] font-medium">PRECISION RENDERING ENGINE V1.0</p>
                        </div>
                    </div>

                    {/* Side Info */}
                    <div className="space-y-8">
                        <div className="zen-glass p-8 space-y-6">
                            <div className="flex items-center justify-between">
                                <h3 className="font-bold flex items-center gap-2"><Star className="w-4 h-4 text-amber-500" /> 智能判局</h3>
                                <span className="text-[10px] text-zinc-300 font-bold uppercase tracking-wider">Analysis</span>
                            </div>
                            <div className="space-y-4">
                                <div className="p-4 bg-zinc-50 rounded-2xl border border-white space-y-1">
                                    <div className="flex justify-between items-center">
                                        <span className="text-sm font-bold text-zinc-800">格局识别 (锁)</span>
                                        <Zap className="w-3 h-3 text-amber-400" />
                                    </div>
                                    <p className="text-xs text-zinc-400 leading-relaxed font-light">升级尊享版以获取高阶格局自动识别算法。</p>
                                </div>
                            </div>
                        </div>

                        <div className="zen-glass p-8">
                            <h3 className="font-bold text-zinc-800 mb-6">历史背景数据</h3>
                            <div className="space-y-6 h-64 overflow-y-auto pr-2">
                                {[1, 2, 3].map(i => (
                                    <div key={i} className="flex gap-4 items-start pb-6 border-b border-zinc-50 last:border-0">
                                        <div className="w-1 bg-zinc-100 h-10 rounded-full" />
                                        <div className="space-y-1">
                                            <div className="text-xs font-bold text-zinc-800">未命名的推演案件 {i}</div>
                                            <div className="text-[10px] text-zinc-300">2026.02.24 12:00:00</div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
