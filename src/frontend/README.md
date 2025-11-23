# Stock Trading AI Assistant - Frontend

A modern, AI-powered stock trading assistant built with Next.js 15, featuring real-time chat interactions, stock recommendations, and detailed analytics.

## 🚀 Features

### Chat Interface
- **Real-time AI Chat**: Interactive conversations with an AI trading assistant
- **Chat History**: Browse and continue previous conversations
- **Contextual Responses**: AI analyzes your questions and provides personalized stock recommendations
- **Report Generation**: Generate comprehensive stock reports from chat conversations

### Stock Reports
- **AI-Driven Recommendations**: View curated stock recommendations with AI rankings
- **Sortable Data Tables**: Sort stocks by symbol, sector, signal, AI-Rank, Sharpe ratio, CAGR, and max drawdown
- **Pagination**: Flexible results per page (5, 10, 25, 50, 100)
- **Report History**: Access and review previously generated reports
- **Color-Coded Signals**: Visual indicators for Buy, Sell, and Hold recommendations

### Stock Detail Pages
- **Candlestick Charts**: Professional stock price visualization with OHLC data
- **Volume Analysis**: Trading volume charts with historical comparisons
- **Time Range Selection**: View data across multiple timeframes (1W, 1M, 3M, 6M, 1Y, YTD, 5Y, MAX)
- **AI Analysis**: Detailed bullet-point explanations for stock recommendations
- **Company Information**: Comprehensive company details, metrics, and descriptions
- **Key Metrics Dashboard**: AI-Rank, Sharpe ratio, CAGR, and Max Drawdown

## 🛠️ Tech Stack

- **Framework**: Next.js 15.5.6 (App Router)
- **Language**: JavaScript/React
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Charts**: Recharts
- **Markdown**: react-markdown with remark-gfm and rehype-raw

## 📋 Prerequisites

- Node.js 18.x or higher
- npm or yarn
- Backend chat agent API (optional - can use mock data)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Install Recharts for charts**
   ```bash
   npm install recharts
   ```

4. **Configure environment variables**
   
   Create a `.env.local` file in the root directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

## 🚦 Running the Application

### Development Mode (with Mock Data)

For testing without a backend:

1. **Update service imports to use MockDataService**
   
   In the following files, change:
   ```javascript
   import DataService from "../../lib/DataService";
   ```
   to:
   ```javascript
   import DataService from "../../lib/MockDataService";
   ```
   
   Files to update:
   - `app/chat/page.jsx`
   - `components/chat/ChatHistory.jsx`
   - `components/chat/ChatHistorySidebar.jsx`
   - `app/report/page.jsx`
   - `components/report/ReportSidebar.jsx`
   - `app/stock-detail/page.jsx`

2. **Start the development server**
   ```bash
   npm run dev
   ```

3. **Open your browser**
   
   Navigate to [http://localhost:3000](http://localhost:3000)

### Production Mode (with Backend API)

1. **Ensure backend is running**
   
   Your backend API should be running and accessible at the URL specified in `.env.local`

2. **Use DataService (not MockDataService)**
   
   Make sure all components import from `DataService`

3. **Build and start**
   ```bash
   npm run build
   npm start
   ```

## 📁 Project Structure

```
frontend/
├── app/
│   ├── chat/
│   │   └── page.jsx              # Main chat page
│   ├── report/
│   │   └── page.jsx              # Stock report page
│   └── stock-detail/
│       └── page.jsx              # Individual stock detail page
├── components/
│   ├── chat/
│   │   ├── ChatHistory.jsx       # Chat history cards
│   │   ├── ChatHistorySidebar.jsx # Chat sidebar navigation
│   │   ├── ChatInput.jsx         # Message input component
│   │   └── ChatMessage.jsx       # Message display component
│   ├── report/
│   │   ├── ReportTable.jsx       # Stock recommendations table
│   │   └── ReportSidebar.jsx     # Report history sidebar
│   ├── stock/
│   │   ├── StockPriceChart.jsx   # Candlestick price chart
│   │   └── StockVolumeChart.jsx  # Volume bar chart
│   └── ui/                       # shadcn/ui components
├── lib/
│   ├── DataService.js            # Production API service
│   ├── MockDataService.js        # Mock data service for testing
│   └── Common.js                 # Utility functions
├── .env.local                    # Environment variables
└── package.json
```

## 🔌 API Integration

### Backend Endpoints Required

Your backend should implement these endpoints:

#### Chat Operations
```
GET    /api/chats?model={model}&limit={limit}
GET    /api/chat/{chatId}?model={model}
POST   /api/chat/start?model={model}
POST   /api/chat/{chatId}/continue?model={model}
```

#### Report Operations
```
GET    /api/reports?model={model}&limit={limit}
GET    /api/report/{reportId}?model={model}
POST   /api/report/generate?model={model}
```

#### Stock Operations
```
GET    /api/stock/{symbol}?model={model}&report_id={reportId}
```

See `lib/DataService.js` for detailed request/response formats.

## 🎨 Features Walkthrough

### 1. Chat with AI Assistant

- Start a conversation about stocks
- Ask questions like "What are the best tech stocks?"
- Receive personalized recommendations
- Continue conversations across sessions

### 2. Generate Stock Reports

- Chat with the AI until it says "please press generate report button"
- Click the "Generate Report" button that appears
- View comprehensive stock recommendations table
- Sort and filter results

### 3. View Stock Details

- Click "More Details" on any stock in a report
- View candlestick price charts
- Analyze trading volume
- Read AI-generated analysis
- Switch between different time ranges

### 4. Time Range Analysis

- Select from 8 time ranges: 1W, 1M, 3M, 6M, 1Y, YTD, 5Y, MAX
- Charts automatically sync and update
- Compare price trends and volume patterns

## 🧪 Testing

### Using Mock Data

The `MockDataService` provides realistic test data:

- **3 sample chats** with message history
- **2 detailed reports** with 8-12 stocks each
- **5 years of price/volume data** for all stocks
- **Realistic stock metrics** and company information

Test URLs:
```
Chat: http://localhost:3000/chat
Report: http://localhost:3000/report?id=report-001
Stock: http://localhost:3000/stock-detail?symbol=AAPL&report_id=report-001
```

### Testing Checklist

- [ ] Navigate to chat page
- [ ] Send a test message
- [ ] View chat history
- [ ] Generate a report (or view mock report)
- [ ] Sort table columns
- [ ] Change pagination (10, 25, 50 items)
- [ ] Click "More Details" on a stock
- [ ] Switch time ranges on charts
- [ ] Navigate back to report
- [ ] Browse report history

## 🎨 Customization

### Color Schemes

The app uses CSS variables for theming. Edit `globals.css`:

```css
:root {
  --primary: your-color;
  --secondary: your-color;
  /* ... */
}
```

### Chart Colors

Edit chart colors in:
- `StockPriceChart.jsx` - Line colors for candlesticks
- `StockVolumeChart.jsx` - Bar colors for volume

### Mock Data

Customize mock data in `lib/MockDataService.js`:
- Add more stocks
- Change company descriptions
- Modify AI analysis points
- Adjust price data generation

## 📊 Data Models

### Chat Object
```javascript
{
  chat_id: string,
  title: string,
  dts: ISO datetime,
  messages: [
    {
      message_id: string,
      role: "user" | "assistant",
      content: string,
      timestamp: ISO datetime
    }
  ]
}
```

### Report Object
```javascript
{
  report_id: string,
  title: string,
  generated_date: ISO datetime,
  chat_id: string,
  stocks: [
    {
      symbol: string,
      sector: string,
      signal: "Strong Buy" | "Buy" | "Hold" | "Sell",
      ai_rank: number,
      sharpe: number,
      cagr: number,
      max_drawdown: number
    }
  ]
}
```

### Stock Detail Object
```javascript
{
  symbol: string,
  stock_name: string,
  company_name: string,
  sector: string,
  industry: string,
  market_cap: string,
  exchange: string,
  signal: string,
  ai_rank: number,
  sharpe: number,
  cagr: number,
  max_drawdown: number,
  description: string,
  ai_analysis: string[],
  price_data: [...],
  volume_data: [...]
}
```

## 🐛 Troubleshooting

### "Failed to fetch" errors

**Problem**: Components are trying to call API but backend isn't running

**Solution**: 
1. Switch to `MockDataService` in component imports
2. OR ensure backend is running at the URL in `.env.local`
3. Check CORS settings on backend

### Charts not displaying

**Problem**: Recharts not installed

**Solution**: 
```bash
npm install recharts
```

### Styling issues

**Problem**: Tailwind classes not applying

**Solution**: 
1. Check `tailwind.config.js` is configured
2. Ensure CSS is imported in layout
3. Verify shadcn/ui components are installed

### No data showing

**Problem**: Mock data not loading

**Solution**: 
1. Verify imports are pointing to `MockDataService`
2. Check browser console for errors
3. Clear browser cache and restart dev server

## 🚀 Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Add environment variables
4. Deploy

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

Build and run:
```bash
docker build -t stock-assistant-frontend .
docker run -p 3000:3000 stock-assistant-frontend
```

## 📝 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000/api` | Yes |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

[Your License Here]

## 👥 Authors

[Your Name/Team]

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Email: [your-email]
- Documentation: [your-docs-url]

## 🗺️ Roadmap

- [ ] Real-time price updates via WebSocket
- [ ] Portfolio tracking
- [ ] Advanced technical indicators
- [ ] Export reports to PDF
- [ ] Dark/Light theme toggle
- [ ] Multi-language support
- [ ] Mobile app version

---

Built with ❤️ using Next.js and AI