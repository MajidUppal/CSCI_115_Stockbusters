'use client';

import { useState, use, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ReportTable from '@/components/report/ReportTable';
import ReportSidebar from '@/components/report/ReportSidebar';
//import DataService from "../../lib/DataService";
import DataService from "../../lib/MockDataService";

const MODEL = 'llm'; // Single model constant

export default function ReportPage({ searchParams }) {
    const params = use(searchParams);
    const report_id = params.id;
    const router = useRouter();

    // Component States
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(false);

    const fetchReport = async (id) => {
        try {
            setLoading(true);
            const response = await DataService.GetReport(MODEL, id);
            setReport(response.data);
        } catch (error) {
            console.error('Error fetching report:', error);
            setReport(null);
        } finally {
            setLoading(false);
        }
    };

    // Setup Component
    useEffect(() => {
        if (report_id) {
            fetchReport(report_id);
        }
    }, [report_id]);

    return (
        <div className="h-screen flex flex-col">
            <div className="flex h-[calc(100vh-64px)]">
                {/* Sidebar */}
                <div className="w-80 flex-shrink-0 bg-card border-r border-border">
                    <ReportSidebar report_id={report_id} />
                </div>

                {/* Main Report Area */}
                <div className="flex-1 flex flex-col h-full overflow-hidden">
                    {/* Header */}
                    <div className="flex-shrink-0 bg-gradient-to-r from-primary/10 via-primary/5 to-transparent border-b border-border">
                        <div className="p-8">
                            <h1 className="text-4xl font-bold gradient-text mb-2">
                                Stock Recommendations 📈
                            </h1>
                            <p className="text-muted-foreground text-lg">
                                Powered by AI-driven analysis • Maximize your portfolio potential
                            </p>
                            {report && (
                                <div className="mt-4 flex items-center gap-4 text-sm">
                                    <span className="text-foreground">
                                        Report Date: {new Date(report.generated_date).toLocaleDateString()}
                                    </span>
                                    <span className="text-muted-foreground">•</span>
                                    <span className="text-foreground">
                                        Total Recommendations: {report.stocks?.length || 0}
                                    </span>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Report Content */}
                    <div className="flex-1 overflow-hidden">
                        {loading ? (
                            <div className="flex items-center justify-center h-full">
                                <div className="text-center">
                                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
                                    <p className="mt-4 text-muted-foreground">Loading report...</p>
                                </div>
                            </div>
                        ) : report ? (
                            <ReportTable stocks={report.stocks || []} />
                        ) : (
                            <div className="flex items-center justify-center h-full">
                                <div className="text-center">
                                    <p className="text-muted-foreground text-lg">No report selected</p>
                                    <p className="text-sm text-muted-foreground mt-2">
                                        Select a report from the sidebar or generate a new one
                                    </p>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}