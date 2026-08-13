'use client';

import React, { useEffect, useState } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';
import { Phone, CheckCircle, XCircle, Activity, RefreshCw } from 'lucide-react';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function Dashboard() {
  const [stats, setStats] = useState({ total: 0, successful: 0, failed: 0 });
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/stats');
      const data = await res.json();
      if (data.success && data.stats) {
        setStats(data.stats);
      }
    } catch (e) {
      console.error('Failed to fetch stats', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 10000); // Live updates every 10s
    return () => clearInterval(interval);
  }, []);

  const chartData = {
    labels: ['Successful Calls', 'Failed Calls'],
    datasets: [
      {
        data: [stats.successful, stats.failed],
        backgroundColor: ['#10b981', '#ef4444'],
        borderColor: ['#059669', '#dc2626'],
        borderWidth: 1,
        hoverOffset: 4,
      },
    ],
  };

  const chartOptions = {
    cutout: '75%',
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          color: '#e5e7eb',
          font: { family: 'inherit', size: 14 }
        }
      }
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-8 font-sans selection:bg-emerald-500/30">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
              Agent Telemetry Dashboard
            </h1>
            <p className="text-slate-400 mt-2 text-lg">Real-time performance metrics for Shiksha AI</p>
          </div>
          <button 
            onClick={fetchStats}
            className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 transition-colors px-4 py-2 rounded-lg border border-slate-700 shadow-sm text-sm font-medium"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl -mr-16 -mt-16 transition-opacity group-hover:bg-blue-500/20"></div>
            <div className="flex items-center justify-between relative z-10">
              <div>
                <p className="text-sm font-medium text-slate-400">Total Calls</p>
                <div className="flex items-baseline gap-2 mt-2">
                  <span className="text-5xl font-black text-white">{stats.total}</span>
                </div>
              </div>
              <div className="w-14 h-14 rounded-full bg-blue-500/20 flex items-center justify-center border border-blue-500/30">
                <Phone className="w-6 h-6 text-blue-400" />
              </div>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl -mr-16 -mt-16 transition-opacity group-hover:bg-emerald-500/20"></div>
            <div className="flex items-center justify-between relative z-10">
              <div>
                <p className="text-sm font-medium text-slate-400">Successful Calls</p>
                <div className="flex items-baseline gap-2 mt-2">
                  <span className="text-5xl font-black text-white">{stats.successful}</span>
                </div>
              </div>
              <div className="w-14 h-14 rounded-full bg-emerald-500/20 flex items-center justify-center border border-emerald-500/30">
                <CheckCircle className="w-6 h-6 text-emerald-400" />
              </div>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/10 rounded-full blur-3xl -mr-16 -mt-16 transition-opacity group-hover:bg-red-500/20"></div>
            <div className="flex items-center justify-between relative z-10">
              <div>
                <p className="text-sm font-medium text-slate-400">Failed Calls</p>
                <div className="flex items-baseline gap-2 mt-2">
                  <span className="text-5xl font-black text-white">{stats.failed}</span>
                </div>
              </div>
              <div className="w-14 h-14 rounded-full bg-red-500/20 flex items-center justify-center border border-red-500/30">
                <XCircle className="w-6 h-6 text-red-400" />
              </div>
            </div>
          </div>

        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col items-center">
            <h3 className="text-lg font-semibold text-slate-300 w-full mb-6">Outcome Distribution</h3>
            <div className="w-64 h-64 relative flex items-center justify-center">
              {stats.total > 0 ? (
                <>
                  <Doughnut data={chartData} options={chartOptions} />
                  <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none mt-[-10px]">
                    <span className="text-3xl font-bold">{Math.round((stats.successful / max(stats.total, 1)) * 100)}%</span>
                    <span className="text-xs text-slate-400 uppercase tracking-wider">Success</span>
                  </div>
                </>
              ) : (
                <div className="flex flex-col items-center text-slate-500">
                  <Activity className="w-8 h-8 mb-2 opacity-50" />
                  <p>No calls recorded yet</p>
                </div>
              )}
            </div>
          </div>
          
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-center">
            <h3 className="text-lg font-semibold text-slate-300 mb-4">LiveKit & SQLite Telemetry</h3>
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/50">
                <p className="text-sm text-slate-400 mb-1">Total Call Volume processed locally via SQLite</p>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${Math.min(stats.total * 2, 100)}%` }}></div>
                </div>
              </div>
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/50">
                <p className="text-sm text-slate-400 mb-1">Target Success Rate</p>
                <div className="flex items-center gap-4">
                  <div className="w-full bg-slate-800 rounded-full h-2 flex-grow">
                    <div className="bg-emerald-500 h-2 rounded-full" style={{ width: `${Math.round((stats.successful / max(stats.total, 1)) * 100)}%` }}></div>
                  </div>
                  <span className="text-emerald-400 text-sm font-medium">{Math.round((stats.successful / max(stats.total, 1)) * 100)}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function max(a: number, b: number) {
  return a > b ? a : b;
}
