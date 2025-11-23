'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { FileText, Plus } from 'lucide-react';
//import DataService from "../../lib/DataService";
import DataService from "../../lib/MockDataService";
import { formatRelativeTime } from "../../lib/Common";

const MODEL = 'llm'; // Single model constant

export default function ReportSidebar({ report_id }) {
    // Component States
    const [reports, setReports] = useState([]);
    const router = useRouter();

    // Setup Component
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await DataService.GetReports(MODEL, 20);
                setReports(response.data);
            } catch (error) {
                console.error('Error fetching reports:', error);
                setReports([]); // Set empty array in case of error
            }
        };

        fetchData();
    }, []);

    return (
        <div className="flex flex-col h-full bg-card border-r border-border">
            <div className="flex items-center justify-between p-4 bg-muted border-b border-border">
                <h2 className="text-foreground text-lg flex items-center gap-2">
                    <FileText className="text-primary w-5 h-5" />
                    Reports History
                </h2>
                <button
                    onClick={() => router.push('/chat')}
                    className="flex items-center gap-1 px-3 py-1.5 bg-primary text-primary-foreground hover:bg-primary/90
                        rounded-lg transition-colors text-sm"
                    title="Go to chat to generate new report"
                >
                    <Plus className="w-4 h-4" />
                    New
                </button>
            </div>

            <div className="flex-1 overflow-y-auto">
                {reports.length === 0 ? (
                    <div className="p-4 text-center text-muted-foreground text-sm">
                        No reports yet. Start a chat to generate your first report.
                    </div>
                ) : (
                    reports.map((report) => (
                        <div
                            key={report.report_id}
                            onClick={() => router.push(`/report?id=${report.report_id}`)}
                            className={`p-4 border-b border-border cursor-pointer hover:bg-muted/50
                              transition-colors ${report_id === report.report_id ? 'bg-accent' : ''}`}
                        >
                            <div className="flex flex-col gap-2">
                                <div className="flex items-start justify-between gap-2">
                                    <span className="text-foreground text-sm font-medium line-clamp-2">
                                        {report.title || 'Stock Recommendations Report'}
                                    </span>
                                    {report.stock_count && (
                                        <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded-full whitespace-nowrap">
                                            {report.stock_count} stocks
                                        </span>
                                    )}
                                </div>
                                <span className="text-muted-foreground text-xs">
                                    {formatRelativeTime(report.generated_date)}
                                </span>
                                {report.chat_id && (
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            router.push(`/chat?id=${report.chat_id}`);
                                        }}
                                        className="text-xs text-primary hover:underline text-left"
                                    >
                                        View source chat →
                                    </button>
                                )}
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}