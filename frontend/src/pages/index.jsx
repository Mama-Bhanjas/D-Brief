import Head from 'next/head';
import React, { useState } from 'react';
import SummaryCard from '../components/SummaryCard';
import CategoryTabs from '../components/CategoryTabs';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { ChevronRight, BarChart3, Users, CheckCircle } from 'lucide-react';

export default function Home() {
    const [category, setCategory] = useState('all');

    // Dummy data
    const reports = [
        { id: 1, title: 'Flood in Sector 4', description: 'Severe water logging observed.', category: 'flood', timestamp: Date.now() - 3600000, location: 'Mumbai' },
        { id: 2, title: 'Building crack observed', description: 'Large crack appeared after tremors.', category: 'earthquake', timestamp: Date.now() - 7200000, location: 'Delhi' },
        // Add more dummy items if needed
    ];

    const filteredReports = category === 'all'
        ? reports
        : reports.filter(r => r.category === category);

    const container = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const item = {
        hidden: { opacity: 0, y: 20 },
        show: { opacity: 1, y: 0 }
    };

    return (
        <div className="space-y-12 pb-12">
            <Head>
                <title>Mama-Bhanjas Dashboard</title>
                <meta name="description" content="Disaster reporting and verification platform" />
            </Head>

            {/* Hero Section */}
            <section className="relative overflow-hidden bg-surface-900 text-white rounded-3xl mx-4 sm:mx-6 lg:mx-8 shadow-2xl">
                <div className="absolute inset-0 bg-gradient-to-br from-primary-600 to-indigo-900 opacity-90"></div>
                <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-primary-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
                <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-80 h-80 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>

                <div className="relative z-10 px-8 py-16 sm:px-16 sm:py-24 text-center">
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-4xl sm:text-6xl font-extrabold tracking-tight mb-6"
                    >
                        Decentralized Disaster Response
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        className="text-lg sm:text-xl text-primary-100 max-w-2xl mx-auto mb-10"
                    >
                        Verify incidents in real-time using blockchain technology. Report disasters, validate claims, and help your community faster.
                    </motion.p>
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="flex flex-col sm:flex-row justify-center gap-4"
                    >
                        <Link href="/submit" className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-full text-primary-700 bg-white hover:bg-gray-50 transition-all shadow-lg hover:shadow-xl">
                            Report Incident
                        </Link>
                        <Link href="/verify" className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-full text-white bg-primary-600 bg-opacity-20 hover:bg-opacity-30 backdrop-blur-sm border-white/20 transition-all">
                            Verify Reports <ChevronRight className="ml-2 h-4 w-4" />
                        </Link>
                    </motion.div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-4">
                        <div className="p-3 bg-blue-100 text-blue-600 rounded-xl">
                            <BarChart3 className="h-6 w-6" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500 font-medium">Total Reports</p>
                            <h4 className="text-2xl font-bold text-gray-900">1,024</h4>
                        </div>
                    </div>
                    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-4">
                        <div className="p-3 bg-green-100 text-green-600 rounded-xl">
                            <CheckCircle className="h-6 w-6" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500 font-medium">Verified Events</p>
                            <h4 className="text-2xl font-bold text-gray-900">856</h4>
                        </div>
                    </div>
                    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-4">
                        <div className="p-3 bg-purple-100 text-purple-600 rounded-xl">
                            <Users className="h-6 w-6" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500 font-medium">Active Verifiers</p>
                            <h4 className="text-2xl font-bold text-gray-900">342</h4>
                        </div>
                    </div>
                </div>
            </section>

            {/* Recent Activity */}
            <section className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex flex-col sm:flex-row justify-between items-center mb-8">
                    <h2 className="text-2xl font-bold text-gray-900 mb-4 sm:mb-0">Recent Activity</h2>
                    <CategoryTabs activeCategory={category} onCategoryChange={setCategory} />
                </div>

                <motion.div
                    variants={container}
                    initial="hidden"
                    animate="show"
                    className="grid gap-6 md:grid-cols-2 lg:grid-cols-3"
                >
                    {filteredReports.map(report => (
                        <motion.div key={report.id} variants={item}>
                            <SummaryCard report={report} />
                        </motion.div>
                    ))}
                </motion.div>
            </section>
        </div>
    );
}
