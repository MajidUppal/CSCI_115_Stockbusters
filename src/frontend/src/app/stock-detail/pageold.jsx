'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { ArrowLeft, TrendingUp, Building2, Sparkles, AlertCircle } from 'lucide-react';
import StockPriceChart from '@/components/stock/StockPriceChart';
import StockVolumeChart from '@/components/stock/StockVolumeChart';
import DataService from "../../lib/DataService";

export default function StockDetailPage() {
    const searchParams = useSearchParams();
    const symbol = searchParams.get('symbol');
    const shortTerm = searchParams.get('short_term') === 'true';
    const longTerm = searchParams.get('long_term') === 'true';
    const router = useRouter();

    // Component States
    const [stockData, setStockData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [timeRange, setTimeRange] = useState('1M');

    const fetchStockDetail = async (ticker) => {
        try {
            setLoading(true);
            setError(null);
            
            console.log('Fetching stock details for:', ticker);
            const response = await DataService.GetStockDetails(ticker);
            console.log('API Response:', response.data);
            
            // Backend returns: { company_profile: {...}, stocks_data: {...}, quant_model: {...} }
            setStockData(response.data);
        } catch (err) {
            console.error('Error fetching stock detail:', err);
            const errorMessage = err.response?.data?.message || err.message || 'Failed to load stock details';
            setError(errorMessage);
            setStockData(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (symbol) {
            fetchStockDetail(symbol);
        } else {
            setError('No stock symbol provided');
        }
    }, [symbol]);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
                    <p className="mt-4 text-muted-foreground">Loading stock details for {symbol}...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex items-center justify-center h-screen p-6">
                <div className="max-w-md w-full bg-card border border-destructive rounded-lg p-8">
                    <AlertCircle className="w-16 h-16 text-destructive mx-auto mb-4" />
                    <h2 className="text-2xl font-bold text-foreground mb-2 text-center">Error Loading Data</h2>
                    <p className="text-muted-foreground mb-6 text-center">{error}</p>
                    <button
                        onClick={() => router.back()}
                        className="w-full px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
                    >
                        Go Back to Report
                    </button>
                </div>
            </div>
        );
    }

    if (!stockData) {
        return (
            <div className="flex items-center justify-center h-screen">
                <div className="text-center">
                    <p className="text-muted-foreground text-lg">No stock details available</p>
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

    // Extract data from the API response structure
    const companyProfile = stockData.company_profile || {};
    const quantModel = stockData.quant_model || {};
    const stocksData = stockData.stocks_data || {};

    // Transform stocks_data from separate arrays to array of objects for charts
    const transformStocksData = (data) => {
        if (!data || !data.date || data.date.length === 0) {
            return { priceData: [], volumeData: [] };
        }

        const priceData = [];
        const volumeData = [];

        for (let i = 0; i < data.date.length; i++) {
            // Format date to readable format (YYYY-MM-DD)
            const dateStr = data.date[i] ? new Date(data.date[i]).toISOString().split('T')[0] : '';
            
            // Price data for candlestick chart
            if (data.open && data.high && data.low && data.close) {
                priceData.push({
                    date: dateStr,
                    open: data.open[i] || 0,
                    high: data.high[i] || 0,
                    low: data.low[i] || 0,
                    close: data.close[i] || 0
                });
            }

            // Volume data for volume chart
            if (data.volume) {
                volumeData.push({
                    date: dateStr,
                    volume: data.volume[i] || 0
                });
            }
        }

        return { priceData, volumeData };
    };

    const { priceData, volumeData } = transformStocksData(stocksData);

    // Determine which AI Score to display based on user preference
    const getAIScore = () => {
        if (shortTerm) {
            // Short-term: use Technical_Score
            return quantModel.Technical_Score;
        } else if (longTerm) {
            // Long-term: use Fundamental_Score  
            return quantModel.Fundamental_Score;
        } else {
            // Default: use Hybrid_Score
            return quantModel.Hybrid_Score;
        }
    };

    const aiScore = getAIScore();
    const aiScoreLabel = shortTerm ? 'AI Score (Technical)' : longTerm ? 'AI Score (Fundamental)' : 'AI Score (Hybrid)';

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
                        {companyProfile.name || symbol} Analysis 📊
                    </h1>
                    
                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2">
                            <span className="text-2xl font-bold text-foreground">
                                {symbol}
                            </span>
                            {quantModel.signal && (
                                <span className="px-3 py-1 rounded-full text-sm font-medium bg-primary/10 text-primary">
                                    {quantModel.signal}
                                </span>
                            )}
                        </div>
                        {companyProfile.name && (
                            <>
                                <div className="text-muted-foreground">•</div>
                                <p className="text-lg text-muted-foreground">
                                    {companyProfile.name}
                                </p>
                            </>
                        )}
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
                                {companyProfile.sector && (
                                    <div>
                                        <span className="text-muted-foreground">Sector:</span>
                                        <span className="ml-2 text-foreground font-medium">
                                            {companyProfile.sector}
                                        </span>
                                    </div>
                                )}
                                {companyProfile.industry && (
                                    <div>
                                        <span className="text-muted-foreground">Industry:</span>
                                        <span className="ml-2 text-foreground font-medium">
                                            {companyProfile.industry}
                                        </span>
                                    </div>
                                )}
                                {companyProfile.market_cap && (
                                    <div>
                                        <span className="text-muted-foreground">Market Cap:</span>
                                        <span className="ml-2 text-foreground font-medium">
                                            {companyProfile.market_cap}
                                        </span>
                                    </div>
                                )}
                                {companyProfile.exchange && (
                                    <div>
                                        <span className="text-muted-foreground">Exchange:</span>
                                        <span className="ml-2 text-foreground font-medium">
                                            {companyProfile.exchange}
                                        </span>
                                    </div>
                                )}
                            </div>
                            
                            {companyProfile.description && (
                                <div className="mt-4 pt-4 border-t border-border">
                                    <p className="text-sm text-muted-foreground leading-relaxed">
                                        {companyProfile.description}
                                    </p>
                                </div>
                            )}
                        </div>

                        {/* Key Metrics */}
                        <div className="bg-card rounded-xl p-6 border border-border shadow-sm">
                            <h2 className="flex items-center gap-2 text-xl font-semibold text-foreground mb-4">
                                <TrendingUp className="w-5 h-5 text-primary" />
                                Key Metrics
                            </h2>
                            <div className="grid grid-cols-2 gap-4">
                                {aiScore !== undefined && (
                                    <div className="bg-muted/50 rounded-lg p-3">
                                        <p className="text-xs text-muted-foreground mb-1">{aiScoreLabel}</p>
                                        <p className="text-lg font-bold text-foreground">
                                            {typeof aiScore === 'number' 
                                                ? aiScore.toFixed(2) 
                                                : aiScore}
                                        </p>
                                    </div>
                                )}
                                {(quantModel.sharpe_1m_annual !== undefined || quantModel.sharpe !== undefined) && (
                                    <div className="bg-muted/50 rounded-lg p-3">
                                        <p className="text-xs text-muted-foreground mb-1">Sharpe Ratio</p>
                                        <p className="text-lg font-bold text-foreground">
                                            {typeof (quantModel.sharpe_1m_annual || quantModel.sharpe) === 'number' 
                                                ? (quantModel.sharpe_1m_annual || quantModel.sharpe).toFixed(2) 
                                                : (quantModel.sharpe_1m_annual || quantModel.sharpe)}
                                        </p>
                                    </div>
                                )}
                                {quantModel.cagr !== undefined && (
                                    <div className="bg-muted/50 rounded-lg p-3">
                                        <p className="text-xs text-muted-foreground mb-1">CAGR</p>
                                        <p className="text-lg font-bold text-green-600 dark:text-green-400">
                                            {typeof quantModel.cagr === 'number' 
                                                ? `${quantModel.cagr.toFixed(2)}%` 
                                                : quantModel.cagr}
                                        </p>
                                    </div>
                                )}
                                {quantModel.max_drawdown !== undefined && (
                                    <div className="bg-muted/50 rounded-lg p-3">
                                        <p className="text-xs text-muted-foreground mb-1">Max Drawdown</p>
                                        <p className="text-lg font-bold text-red-600 dark:text-red-400">
                                            {typeof quantModel.max_drawdown === 'number' 
                                                ? `${quantModel.max_drawdown.toFixed(2)}%` 
                                                : quantModel.max_drawdown}
                                        </p>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* AI Analysis */}
                        {quantModel.reg_reasoning && (
                            <div className="bg-card rounded-xl p-6 border border-border shadow-sm">
                                <h2 className="flex items-center gap-2 text-xl font-semibold text-foreground mb-4">
                                    <Sparkles className="w-5 h-5 text-primary" />
                                    AI-Generated Analysis
                                </h2>
                                <div className="space-y-3">
                                    {quantModel.reg_reasoning.split(/\n|\.(?=\s+[A-Z])/).filter(line => line.trim()).map((point, index) => (
                                        <div key={index} className="flex gap-3">
                                            <div className="flex-shrink-0 w-2 h-2 rounded-full bg-primary mt-2" />
                                            <p className="text-sm text-foreground leading-relaxed">
                                                {point.trim()}{point.trim().endsWith('.') ? '' : '.'}
                                            </p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
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
                        {priceData && priceData.length > 0 && (
                            <div className="bg-card rounded-xl p-6 border border-border shadow-sm">
                                <h2 className="text-xl font-semibold text-foreground mb-4">
                                    Stock Price Trend
                                </h2>
                                <StockPriceChart 
                                    priceData={priceData} 
                                    symbol={symbol}
                                    timeRange={timeRange}
                                />
                            </div>
                        )}

                        {/* Volume Chart */}
                        {volumeData && volumeData.length > 0 && (
                            <div className="bg-card rounded-xl p-6 border border-border shadow-sm">
                                <h2 className="text-xl font-semibold text-foreground mb-4">
                                    Trading Volume Analysis
                                </h2>
                                <StockVolumeChart 
                                    volumeData={volumeData}
                                    symbol={symbol}
                                    timeRange={timeRange}
                                />
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}