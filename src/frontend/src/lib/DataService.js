import axios from 'axios';

// Get API base URL from environment variable or default
// Uses NEXT_PUBLIC_BASE_API_URL to match .env files
const API_BASE_URL = process.env.NEXT_PUBLIC_BASE_API_URL || 'http://localhost:9000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const DataService = {
  // Chat-related methods
  async GetChats(model, limit = 100) {
    try {
      const response = await apiClient.get(`/${model}/chats?limit=${limit}`);
      return response;
    } catch (error) {
      console.error('Error fetching chats:', error);
      throw error;
    }
  },

  async GetChat(model, chatId) {
    try {
      const response = await apiClient.get(`/${model}/chats/${chatId}`);
      return response;
    } catch (error) {
      console.error('Error fetching chat:', error);
      throw error;
    }
  },

  async CreateChat(model, message) {
    try {
      const response = await apiClient.post(`/${model}/chats`, { message });
      return response;
    } catch (error) {
      console.error('Error creating chat:', error);
      throw error;
    }
  },

  async SendMessage(model, chatId, message) {
    try {
      const response = await apiClient.post(`/${model}/chats/${chatId}`, { message });
      return response;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  GetChatMessageImage(model, imagePath) {
    // Construct image URL - adjust based on your API structure
    if (!imagePath) return '';
    if (imagePath.startsWith('http')) return imagePath;
    return `${API_BASE_URL}/${model}/images/${imagePath}`;
  },

  // Stock-related methods
  async GetStockDetails(ticker) {
    try {
      const response = await apiClient.get(`/details/${ticker}`);
      return response;
    } catch (error) {
      console.error('Error fetching stock details:', error);
      throw error;
    }
  },

  async GetStockData(symbol, days = 90) {
    try {
      // This might call a different endpoint or process the stock details
      const response = await apiClient.get(`/details/${symbol}`);
      // Transform the response to match expected format
      return {
        data: response.data?.stocks_data || [],
      };
    } catch (error) {
      console.error('Error fetching stock data:', error);
      throw error;
    }
  },

  async GetStockMetrics(symbol) {
    try {
      const response = await apiClient.get(`/details/${symbol}`);
      // Extract metrics from the response
      const stocksData = response.data?.stocks_data || {};
      return {
        data: {
          price: stocksData.current_price || 0,
          change: stocksData.change || 0,
          changePercent: stocksData.change_percent || 0,
          marketCap: stocksData.market_cap || 0,
          volume: stocksData.volume || 0,
          pe: stocksData.pe_ratio || 0,
          beta: stocksData.beta || 0,
          low52Week: stocksData.low_52_week || 0,
          high52Week: stocksData.high_52_week || 0,
          dividend: stocksData.dividend_yield || 0,
        },
      };
    } catch (error) {
      console.error('Error fetching stock metrics:', error);
      throw error;
    }
  },

  async GetMovingAverages(symbol) {
    try {
      const response = await apiClient.get(`/details/${symbol}`);
      // Extract moving averages from quant_model or calculate them
      const quantData = response.data?.quant_model || {};
      return {
        data: {
          sma20: quantData.sma20 || 0,
          sma50: quantData.sma50 || 0,
          ema12: quantData.ema12 || 0,
          ema26: quantData.ema26 || 0,
        },
      };
    } catch (error) {
      console.error('Error fetching moving averages:', error);
      throw error;
    }
  },

  async GetTechnicalIndicators(symbol) {
    try {
      const response = await apiClient.get(`/details/${symbol}`);
      // Extract technical indicators from quant_model
      const quantData = response.data?.quant_model || {};
      return {
        data: {
          rsi: quantData.rsi || 50,
          macd: quantData.macd || 0,
          signal: quantData.macd_signal || 0,
          bollingerUpper: quantData.bollinger_upper || 0,
          bollingerMiddle: quantData.bollinger_middle || 0,
          bollingerLower: quantData.bollinger_lower || 0,
        },
      };
    } catch (error) {
      console.error('Error fetching technical indicators:', error);
      throw error;
    }
  },

  GetStockList() {
    // Return a static list of stocks - you may want to fetch this from an API
    return [
      { symbol: 'AAPL', name: 'Apple Inc.', sector: 'Technology' },
      { symbol: 'GOOGL', name: 'Alphabet Inc.', sector: 'Technology' },
      { symbol: 'MSFT', name: 'Microsoft Corporation', sector: 'Technology' },
      { symbol: 'AMZN', name: 'Amazon.com Inc.', sector: 'Consumer Cyclical' },
      { symbol: 'TSLA', name: 'Tesla Inc.', sector: 'Consumer Cyclical' },
      { symbol: 'META', name: 'Meta Platforms Inc.', sector: 'Technology' },
      { symbol: 'NVDA', name: 'NVIDIA Corporation', sector: 'Technology' },
      { symbol: 'JPM', name: 'JPMorgan Chase & Co.', sector: 'Financial Services' },
      { symbol: 'V', name: 'Visa Inc.', sector: 'Financial Services' },
      { symbol: 'JNJ', name: 'Johnson & Johnson', sector: 'Healthcare' },
    ];
  },

  // Report-related methods
  async GetReports(model, limit = 20) {
    try {
      const response = await apiClient.get(`/${model}/reports?limit=${limit}`);
      return response;
    } catch (error) {
      console.error('Error fetching reports:', error);
      throw error;
    }
  },

  async GenerateReport(model, chatId, userPreferences) {
    try {
      const response = await apiClient.post(`/${model}/chats/${chatId}/report`, {
        user_pref: userPreferences,
      });
      return response;
    } catch (error) {
      console.error('Error generating report:', error);
      throw error;
    }
  },
};

export default DataService;

