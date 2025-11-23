'use client';

import { useState, use, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, TrendingUp, Building2, Sparkles } from 'lucide-react';
import StockPriceChart from '@/components/stock/StockPriceChart';
import StockVolumeChart from '@/components/stock/StockVolumeChart';
import DataService from "../../lib/MockDataService"; // Use MockDataService for testing

const MODEL = 'llm'; // Single model constant

export default function StockDetailPage({ searchParams }) {
    const params = use(searchParams);
    const symbol = params.symbol;
    const report_id = params.report_id;
    const router = useRouter();

    // Component States
    const [stockDetail, setStockDetail] = useState(null);
    const [loading, setLoading] = useState(false);
    const [timeRange, setTimeRange] = useState('1M'); // Shared time range state

    const fetchStockDetail = async (sym, repId) => {
        try {
            setLoading(true);
            const response = await DataService.GetStockDetail(MODEL, sym, repId);
            setStockDetail(response.data);
        } catch (error) {
            console.error('Error fetching stock detail:', error);
            setStockDetail(null);
        } finally {
            setLoading(false);
        }
    };

    // Setup Component
    useEffect(() => {
        if (symbol && report_id) {
            fetchStockDetail(symbol, report_id);
        }
    }, [symbol, report_id]);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
                    <p className="mt-4 text-muted-foreground">Loading stock details...</p>
                </div>
            </div>
        );
    }

    if (!stockDetail) {
        return (
            <div className="flex items-center justify-center h-screen">
                <div className="text-center">
                    <p className="text-muted-foreground text-lg">Stock details not found</p>
                    <button
                        onClick={() => router.back()}
                        className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
                    >
                        Go Back
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <div className="bg-gradient-to-r from-primary/10 via-primary/5 to-transparent border-b border-border">
                <div className="container mx-auto px-6 py-8">
                    <button
                        onClick={() => router.back()}
                        className="flex items-center gap-2 text-muted-foreground hover:text-foreground mb-4 transition-colors"
                    >
                        <ArrowLeft className="w-4 h-4" />
                        Back to Report
                    </button>
                    
                    <h1 className="text-4xl font-bold gradient-text mb-4">
                        {stockDetail.stock_name} Analysis 📊
                    </h1>
                    
                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2">
                            <span className="text-2xl font-bold text-foreground">
                                {stockDetail.symbol}
                            </span>
                            <span className="px-3 py-1 rounded-full text-sm font-medium bg-primary/10 text-primary">
                                {stockDetail.signal}
                            </span>
                        </div>
                        <div className="text-muted-foreground">•</div>
                        <p className="text-lg text-muted-foreground">
                            {stockDetail.company_name}
                        </p>
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <div className="container mx-auto px-6 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Left Column - Company Info and AI Analysis */}
                    <div className="lg:col-span-1 space-y-6">
                        {/* Company Information */}
                        <div className="bg-card rounded-xl p-6 border border-border shadow-sm">
                            <h2 className="flex items-center gap-2 text-xl font-semibold text-foreground mb-4">
                                <Building2 className="w-5 h-5 text-primary" />
                                Company Information
                            </h2>
                            <div className="space-y-3 text-sm">
                                <div>
                                    <span className="text-muted-foreground">Sector:</span>
                                    <span className="ml-2 text-foreground font-medium">
                                        {stockDetail.sector}
                                    </span>
                                </div>
                                <div>
                                    <span className="text-muted-foreground">Industry:</span>
                                    <span className="ml-2 text-foreground font-medium">
                                        {stockDetail.industry}
                                    </span>
                                </div>
                                <div>
                                    <span className="text-muted-foreground">Market Cap:</span>
                                    <span className="ml-2 text-foreground font-medium">
                                        {stockDetail.market_cap}
                                    </span>
                                </div>
                                <div>
                                    <span className="text-muted-foreground">Exchange:</span>
                                    <span className="ml-2 text-foreground font-medium">
                                        {stockDetail.exchange}
                                    </span>
                                </div>
                            </div>
                            
                            <div className="mt-4 pt-4 border-t border-border">
                                <p className="text-sm text-muted-foreground leading-relaxed">
                                    {stockDetail.description}
                                </p>
                            </div>
                        </div>

                        {/* Key Metrics */}
                        <div className="bg-card rounded-xl p-6 border border-border shadow-sm">
                            <h2 className="flex items-center gap-2 text-xl font-semibold text-foreground mb-4">
                                <TrendingUp className="w-5 h-5 text-primary" />
                                Key Metrics
                            </h2>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-muted/50 rounded-lg p-3">
                                    <p className="text-xs text-muted-foreground mb-1">AI Rank</p>
                                    <p className="text-lg font-bold text-foreground">
                                        {stockDetail.ai_rank}
                                    </p>
                                </div>
                                <div className="bg-muted/50 rounded-lg p-3">
                                    <p className="text-xs text-muted-foreground mb-1">Sharpe Ratio</p>
                                    <p className="text-lg font-bold text-foreground">
                                        {stockDetail.sharpe?.toFixed(2)}
                                    </p>
                                </div>
                                <div className="bg-muted/50 rounded-lg p-3">
                                    <p className="text-xs text-muted-foreground mb-1">CAGR</p>
                                    <p className="text-lg font-bold text-green-600 dark:text-green-400">
                                        {stockDetail.cagr?.toFixed(2)}%
                                    </p>
                                </div>
                                <div className="bg-muted/50 rounded-lg p-3">
                                    <p className="text-xs text-muted-foreground mb-1">Max Drawdown</p>
                                    <p className="text-lg font-bold text-red-600 dark:text-red-400">
                                        {stockDetail.max_drawdown?.toFixed(2)}%
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* AI Analysis */}
                        <div className="bg-card rounded-xl p-6 border border-border shadow-sm">
                            <h2 className="flex items-center gap-2 text-xl font-semibold text-foreground mb-4">
                                <Sparkles className="w-5 h-5 text-primary" />
                                AI-Generated Analysis
                            </h2>
                            <div className="space-y-3">
                                {stockDetail.ai_analysis?.map((point, index) => (
                                    <div key={index} className="flex gap-3">
                                        <div className="flex-shrink-0 w-2 h-2 rounded-full bg-primary mt-2" />
                                        <p className="text-sm text-foreground leading-relaxed">
                                            {point}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Right Column - Charts */}
                    <div className="lg:col-span-2 space-y-6">
                        {/* Time Range Selector - Shared for both charts */}
                        <div className="bg-card rounded-xl p-4 border border-border shadow-sm">
                            <div className="flex items-center justify-between flex-wrap gap-4">
                                <div className="flex gap-2 flex-wrap">
                                    {[
                                        { label: '1W', value: '1W' },
                                        { label: '1M', value: '1M' },
                                        { label: '3M', value: '3M' },
                                        { label: '6M', value: '6M' },
                                        { label: '1Y', value: '1Y' },
                                        { label: 'YTD', value: 'YTD' },
                                        { label: '5Y', value: '5Y' },
                                        { label: 'MAX', value: 'MAX' }
                                    ].map((range) => (
                                        <button
                                            key={range.value}
                                            onClick={() => setTimeRange(range.value)}
                                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                                                timeRange === range.value
                                                    ? 'bg-primary text-primary-foreground shadow-sm'
                                                    : 'bg-muted text-muted-foreground hover:bg-muted/80'
                                            }`}
                                        >
                                            {range.label}
                                        </button>
                                    ))}
                                </div>
                                <div className="text-sm text-muted-foreground">
                                    Time Range: {timeRange}
                                </div>
                            </div>
                        </div>

                        {/* Price Chart */}
                        <div className="bg-card rounded-xl p-6 border border-border shadow-sm">
                            <h2 className="text-xl font-semibold text-foreground mb-4">
                                Stock Price Trend
                            </h2>
                            <StockPriceChart 
                                priceData={stockDetail.price_data} 
                                symbol={stockDetail.symbol}
                                timeRange={timeRange}
                            />
                        </div>

                        {/* Volume Chart */}
                        <div className="bg-card rounded-xl p-6 border border-border shadow-sm">
                            <h2 className="text-xl font-semibold text-foreground mb-4">
                                Trading Volume Analysis
                            </h2>
                            <StockVolumeChart 
                                volumeData={stockDetail.volume_data}
                                symbol={stockDetail.symbol}
                                timeRange={timeRange}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}