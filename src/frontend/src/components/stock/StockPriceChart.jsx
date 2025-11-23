'use client';

import { useState } from 'react';
import { ComposedChart, Bar, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

export default function StockPriceChart({ priceData, symbol, timeRange }) {
    // Time range options
    const timeRanges = [
        { label: '1W', value: '1W', days: 7 },
        { label: '1M', value: '1M', days: 30 },
        { label: '3M', value: '3M', days: 90 },
        { label: '6M', value: '6M', days: 180 },
        { label: '1Y', value: '1Y', days: 365 },
        { label: 'YTD', value: 'YTD', days: null }, // Year to date
        { label: '5Y', value: '5Y', days: 1825 },
        { label: 'MAX', value: 'MAX', days: null }
    ];

    // Filter data based on time range prop from parent
    const getFilteredData = () => {
        if (!priceData || priceData.length === 0) return [];
        
        if (timeRange === 'MAX') {
            return priceData;
        }
        
        if (timeRange === 'YTD') {
            // Filter from Jan 1 of current year
            const currentYear = new Date().getFullYear();
            const startOfYear = new Date(currentYear, 0, 1);
            // For mock data, just return last 90 days as approximation
            return priceData.slice(-90);
        }
        
        const selectedRange = timeRanges.find(r => r.value === timeRange);
        if (!selectedRange || !selectedRange.days) {
            return priceData;
        }
        
        return priceData.slice(-selectedRange.days);
    };

    const filteredData = getFilteredData();

    // Transform data for candlestick representation
    const transformedData = filteredData.map(item => ({
        ...item,
        // Candlestick body range (open to close)
        candleBottom: Math.min(item.open, item.close),
        candleTop: Math.max(item.open, item.close),
        candleHeight: Math.abs(item.close - item.open),
        // Wicks (high to low)
        wickBottom: item.low,
        wickHeight: item.high - item.low,
        // Determine if bullish (green) or bearish (red)
        isBullish: item.close >= item.open
    }));

    // Custom candlestick shape using Bar chart
    const CandleStick = (props) => {
        const { x, y, width, height, payload } = props;
        const centerX = x + width / 2;
        const wickWidth = 2;
        const candleWidth = width * 0.6;
        
        // Calculate positions
        const wickY = payload.wickBottom;
        const candleY = payload.candleBottom;
        
        // Scale calculations (these need to be proportional to chart scale)
        const yScale = height / (payload.high - payload.low);
        const wickHeightPx = payload.wickHeight * yScale;
        const candleHeightPx = payload.candleHeight * yScale;
        
        const color = payload.isBullish ? '#10b981' : '#ef4444'; // green : red
        
        return (
            <g>
                {/* Wick (high-low line) */}
                <line
                    x1={centerX}
                    y1={y}
                    x2={centerX}
                    y2={y + height}
                    stroke={color}
                    strokeWidth={wickWidth}
                />
                {/* Candle body */}
                <rect
                    x={centerX - candleWidth / 2}
                    y={y + (payload.isBullish ? height * ((payload.high - payload.close) / payload.wickHeight) : height * ((payload.high - payload.open) / payload.wickHeight))}
                    width={candleWidth}
                    height={Math.max(candleHeightPx, 1)}
                    fill={payload.isBullish ? '#10b981' : '#ef4444'}
                    stroke={color}
                    strokeWidth={1}
                />
            </g>
        );
    };

    // Custom tooltip
    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            const data = payload[0].payload;
            const priceChange = data.close - data.open;
            const percentChange = ((priceChange / data.open) * 100).toFixed(2);
            
            return (
                <div className="bg-card border border-border rounded-lg p-4 shadow-lg">
                    <p className="text-sm font-semibold text-foreground mb-2">{label}</p>
                    <div className="space-y-1">
                        <div className="flex justify-between gap-4">
                            <span className="text-xs text-muted-foreground">Open:</span>
                            <span className="text-xs text-foreground font-medium">${data.open.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between gap-4">
                            <span className="text-xs text-muted-foreground">High:</span>
                            <span className="text-xs text-blue-600 dark:text-blue-400 font-medium">${data.high.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between gap-4">
                            <span className="text-xs text-muted-foreground">Low:</span>
                            <span className="text-xs text-orange-600 dark:text-orange-400 font-medium">${data.low.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between gap-4">
                            <span className="text-xs text-muted-foreground">Close:</span>
                            <span className="text-xs text-foreground font-medium">${data.close.toFixed(2)}</span>
                        </div>
                        <div className="pt-2 mt-2 border-t border-border flex justify-between gap-4">
                            <span className="text-xs text-muted-foreground">Change:</span>
                            <span className={`text-xs font-semibold ${priceChange >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                                {priceChange >= 0 ? '+' : ''}{priceChange.toFixed(2)} ({percentChange}%)
                            </span>
                        </div>
                    </div>
                </div>
            );
        }
        return null;
    };

    // Calculate price range for Y-axis domain
    const allPrices = filteredData.flatMap(item => [item.high, item.low]);
    const minPrice = Math.min(...allPrices);
    const maxPrice = Math.max(...allPrices);
    const padding = (maxPrice - minPrice) * 0.1; // 10% padding

    return (
        <div className="w-full">
            {/* Chart */}
            <div className="w-full h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                    <ComposedChart
                        data={transformedData}
                        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                        <XAxis 
                            dataKey="date" 
                            className="text-xs text-muted-foreground"
                            tick={{ fill: 'currentColor' }}
                        />
                        <YAxis 
                            domain={[minPrice - padding, maxPrice + padding]}
                            className="text-xs text-muted-foreground"
                            tick={{ fill: 'currentColor' }}
                            label={{ 
                                value: 'Price ($)', 
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
                            payload={[
                                { value: 'Bullish (Green)', type: 'rect', color: '#10b981' },
                                { value: 'Bearish (Red)', type: 'rect', color: '#ef4444' }
                            ]}
                        />
                        {/* Render candlesticks */}
                        <Bar 
                            dataKey="high" 
                            fill="transparent"
                            shape={<CandleStick />}
                        >
                            {transformedData.map((entry, index) => (
                                <Cell key={`cell-${index}`} />
                            ))}
                        </Bar>
                    </ComposedChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}