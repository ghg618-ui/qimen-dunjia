"use client";

import React, { useState } from 'react';
import { Compass, Shield, Zap, ArrowRight, User, Lock, Mail, ChevronRight } from 'lucide-react';
import Dashboard from '../components/Dashboard';

export default function ZenApp() {
    const [isLogged, setIsLogged] = useState(false);
    const [view, setView] = useState('landing');
    const [user] = useState({ email: 'gonghg@apple.com', isVip: true });

    if (isLogged) return <Dashboard user={user} />;

    return (
        <div className="min-h-screen selection:bg-amber-100 flex flex-col items-center justify-center p-6 sm:p-24 overflow-hidden relative">
            {/* Soft Apple-style Gradients */}
            <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-amber-100/30 rounded-full blur-[120px] -z-10" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-50/40 rounded-full blur-[120px] -z-10" />

            {view === 'landing' && (
                <div className="max-w-3xl w-full text-center space-y-12 animate-in fade-in zoom-in-95 duration-1000">
                    <div className="inline-flex p-4 rounded-3xl bg-white shadow-sm border border-gray-100 mb-4">
                        <Compass className="w-8 h-8 text-zinc-800" />
                    </div>

                    <div className="space-y-6">
                        <h1 className="text-5xl md:text-8xl font-bold tracking-tight text-zinc-900">
                            奇门遁甲 <span className="text-zinc-400 font-light">元始版</span>
                        </h1>
                        <p className="text-xl md:text-2xl text-zinc-400 font-light max-w-2xl mx-auto leading-relaxed">
                            在宁静中洞察时空格局。一款为您量身定制的极致简约推演系统。
                        </p>
                    </div>

                    <div className="flex flex-col sm:flex-row gap-6 justify-center pt-8">
                        <button
                            onClick={() => setView('login')}
                            className="apple-btn group flex items-center gap-3"
                        >
                            开启体验 <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                        </button>
                        <button className="px-8 py-4 rounded-2xl border border-zinc-200 font-semibold text-zinc-600 hover:bg-white transition-all">
                            了解设计理念
                        </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-12 pt-24 text-left">
                        <div className="space-y-3">
                            <div className="w-8 h-8 bg-zinc-100 rounded-lg flex items-center justify-center"><Zap className="w-4 h-4 text-zinc-400" /></div>
                            <h3 className="font-bold text-zinc-800">极致性能</h3>
                            <p className="text-sm text-zinc-400 leading-relaxed font-light">毫秒级实时起局，毫秒级数据同步，从未如此丝滑。</p>
                        </div>
                        <div className="space-y-3">
                            <div className="w-8 h-8 bg-zinc-100 rounded-lg flex items-center justify-center"><Shield className="w-4 h-4 text-zinc-400" /></div>
                            <h3 className="font-bold text-zinc-800">安全私密</h3>
                            <p className="text-sm text-zinc-400 leading-relaxed font-light">所有数据在云端采用端到端加密，您的机密仅属于您。</p>
                        </div>
                        <div className="space-y-3">
                            <div className="w-8 h-8 bg-zinc-100 rounded-lg flex items-center justify-center"><Compass className="w-4 h-4 text-zinc-400" /></div>
                            <h3 className="font-bold text-zinc-800">现代美学</h3>
                            <p className="text-sm text-zinc-400 leading-relaxed font-light">告别复杂视觉，回归推演本质，专注洞察未来。</p>
                        </div>
                    </div>
                </div>
            )}

            {view === 'login' && (
                <div className="w-full max-w-md zen-glass p-12 space-y-10 animate-in slide-in-from-bottom-8 duration-500">
                    <div className="space-y-2 text-center">
                        <h2 className="text-3xl font-bold tracking-tight text-zinc-900">登录账号</h2>
                        <p className="text-sm text-zinc-400 font-light">开启您的禅意科技推演之旅</p>
                    </div>

                    <div className="space-y-6">
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-zinc-400 uppercase tracking-widest ml-1">凭证</label>
                            <input type="email" className="zen-input" placeholder="邮箱地址" defaultValue="demo@qimen.com" />
                        </div>
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-zinc-400 uppercase tracking-widest ml-1">访问码</label>
                            <input type="password" className="zen-input" placeholder="密码" defaultValue="password123" />
                        </div>
                        <button
                            onClick={() => setIsLogged(true)}
                            className="apple-btn w-full mt-4 py-5 shadow-2xl shadow-zinc-200"
                        >
                            登 录
                        </button>
                    </div>

                    <div className="text-center">
                        <button onClick={() => setView('landing')} className="text-sm text-zinc-300 hover:text-zinc-500">
                            取消登录并返回
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
