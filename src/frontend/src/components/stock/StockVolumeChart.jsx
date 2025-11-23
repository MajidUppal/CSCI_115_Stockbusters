'use client';

import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function StockVolumeChart({ volumeData, symbol, timeRange }) {
    // Time range options
    const timeRanges = [
        { label: '1W', value: '1W', days: 7 },
        { label: '1M', value: '1M', days: 30 },
        { label: '3M', value: '3M', days: 90 },
        { label: '6M', value: '6M', days: 180 },
        { label: '1Y', value: '1Y', days: 365 },
        { label: 'YTD', value: 'YTD', days: null },
        { label: '5Y', value: '5Y', days: 1825 },
        { label: 'MAX', value: 'MAX', days: null }
    ];

    // Filter data based on time range prop from parent
    const getFilteredData = () => {
        if (!volumeData || volumeData.length === 0) return [];
        
        if (timeRange === 'MAX') {
            return volumeData;
        }
        
        if (timeRange === 'YTD') {
            return volumeData.slice(-90);
        }
        
        const selectedRange = timeRanges.find(r => r.value === timeRange);
        if (!selectedRange || !selectedRange.days) {
            return volumeData;
        }
        
        return volumeData.slice(-selectedRange.days);
    };

    const filteredData = getFilteredData();

    // Custom tooltip
    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            return (
                <div className="bg-card border border-border rounded-lg p-3 shadow-lg">
                    <p className="text-sm font-medium text-foreground mb-1">{label}</p>
                    <p className="text-sm text-primary">
                        Volume: {(payload[0].value / 1000000).toFixed(2)}M
                    </p>
                    {payload[0].payload.avg_volume && (
                        <p className="text-sm text-muted-foreground">
                            Avg: {(payload[0].payload.avg_volume / 1000000).toFixed(2)}M
                        </p>
                    )}
                </div>
            );
        }
        return null;
    };

    // Format large numbers for Y-axis
    const formatYAxis = (value) => {
        if (value >= 1000000) {
            return `${(value / 1000000).toFixed(0)}M`;
        }
        if (value >= 1000) {
            return `${(value / 1000).toFixed(0)}K`;
        }
        return value;
    };

    return (
        <div className="w-full">
            {/* Chart */}
            <div className="w-full h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                        data={filteredData}
                        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                        <XAxis 
                            dataKey="date" 
                            className="text-xs text-muted-foreground"
                            tick={{ fill: 'currentColor' }}
                        />
                        <YAxis 
                            className="text-xs text-muted-foreground"
                            tick={{ fill: 'currentColor' }}
                            tickFormatter={formatYAxis}
                            label={{ 
                                value: 'Volume', 
                                angle: -90, 
                                position: 'insideLeft',
                                style: { textAnchor: 'middle', fill: 'currentColor' }
                            }}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Legend 
                            wrapperStyle={{ 
                                paddingTop: '10px',
                                fontSize: '14px'
                            }}
                        />
                        <Bar 
                            dataKey="volume" 
                            fill="hsl(var(--primary))" 
                            name="Volume"
                            radius={[4, 4, 0, 0]}
                        />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}