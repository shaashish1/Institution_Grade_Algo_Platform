# 📖 AlgoProject User Guide - October 2025 Features

## 🎨 **Multi-Theme User Interface**

### **Theme Selection**
1. **Access Theme Switcher**: Look for the theme icon in the top-right corner of any page
2. **Available Themes**:
   - **Dark Theme**: Professional dark mode with blue accents
   - **Light Theme**: Clean white background with modern typography
   - **Cosmic Theme**: Space-inspired purple gradient with stars
   - **Doodle Theme**: Hand-drawn paper style with animations

### **Theme Features**
- **Automatic Persistence**: Your theme choice is saved in browser localStorage
- **Instant Switching**: Themes change immediately without page reload
- **Responsive Design**: All themes work perfectly on mobile and desktop
- **Animation Support**: Cosmic and Doodle themes include subtle animations

### **Using Themes**
```jsx
// Themes automatically apply to all components
// No additional configuration needed
// Access current theme programmatically:
const { theme, setTheme } = useContext(ThemeContext)
```

---

## 👤 **Individual User Credential Management**

### **Fyers Account Setup**

#### **Getting Your Fyers Credentials:**
1. **Trading Account**: Open account at [Fyers.in](https://fyers.in)
2. **API Credentials**: Visit Fyers Developer Portal
3. **Required Information**:
   - Client ID (e.g., "XA12345-100")
   - Secret Key (from API settings)
   - User Name (trading ID, e.g., "XA00330")
   - 4-digit PIN (trading PIN)
   - TOTP Key (optional, from mobile app)
   - Redirect URI (default: "https://www.google.com")

#### **Adding Your Credentials:**
1. **Navigate**: Go to Settings → Fyers Credentials
2. **Add New User**: Click "Add User Credentials"
3. **Fill Form**: Enter all required information
4. **Save**: Credentials are securely stored locally
5. **Test Connection**: Use "Test Connection" to verify

#### **Managing Multiple Users:**
- **Multiple Accounts**: Support for unlimited user accounts
- **User Selection**: Switch between different trading accounts
- **Individual Settings**: Each user has separate configuration
- **Secure Storage**: Credentials stored in encrypted JSON format

### **User Credential API Endpoints**
```python
# Available endpoints:
POST /fyers/add-user          # Add new user
GET /fyers/list-users         # Get all users
GET /fyers/get-user/{user_id} # Get specific user
PUT /fyers/update-user/{user_id} # Update user
DELETE /fyers/delete-user/{user_id} # Delete user
POST /fyers/test-connection/{user_id} # Test connection
POST /fyers/activate-user/{user_id} # Activate user  
POST /fyers/deactivate-user/{user_id} # Deactivate user
```

---

## 🔐 **Tiered CCXT Authentication System**

### **Trading Modes**

#### **1. Backtest Mode**
- **Purpose**: Historical data analysis and strategy testing
- **Credentials**: Not required
- **Data Access**: Historical price data, indicators, patterns
- **Usage**: Perfect for strategy development and validation

#### **2. Paper Trading Mode**  
- **Purpose**: Live market simulation with fake money
- **Credentials**: Not required
- **Data Access**: Real-time market data for simulation
- **Usage**: Test strategies with live data without risk

#### **3. Live Trading Mode**
- **Purpose**: Real trading with actual funds
- **Credentials**: Required (API keys and secrets)
- **Data Access**: Full trading capabilities
- **Usage**: Execute actual trades with real money

### **Supported Exchanges**
| Exchange | Backtest | Paper | Live Trading |
|----------|----------|-------|--------------|
| Binance | ✅ | ✅ | ✅ (API Key Required) |
| Coinbase Pro | ✅ | ✅ | ✅ (API Key Required) |
| Kraken | ✅ | ✅ | ✅ (API Key Required) |
| KuCoin | ✅ | ✅ | ✅ (API Key Required) |
| OKX | ✅ | ✅ | ✅ (API Key Required) |
| Bybit | ✅ | ✅ | ✅ (API Key Required) |
| Bitfinex | ✅ | ✅ | ✅ (API Key Required) |
| Huobi | ✅ | ✅ | ✅ (API Key Required) |
| Gate.io | ✅ | ✅ | ✅ (API Key Required) |

### **Setting Up Exchange Credentials**
1. **Choose Exchange**: Select from supported exchanges
2. **Create API Keys**: Generate keys in exchange settings
3. **Add Credentials**: Enter API key and secret
4. **Select Trading Mode**: Choose live trading mode
5. **Test Connection**: Verify credentials work

### **Security Features**
- **Mode-Based Validation**: Credentials only required for live trading
- **Secure Storage**: API keys encrypted and stored securely  
- **Connection Testing**: Built-in credential validation
- **Error Handling**: Clear error messages for failed connections

---

## 🤖 **AI Strategy Engine**

### **PineScript Analysis**

#### **Uploading Strategies:**
1. **Navigate**: Go to AI → Strategies page
2. **Upload File**: Click "Upload PineScript Strategy"
3. **Select File**: Choose your `.pine` file
4. **AI Analysis**: Automatic analysis begins
5. **Review Results**: Get comprehensive strategy report

#### **AI Analysis Features:**
- **Strategy Logic Review**: AI examines trading logic
- **Performance Prediction**: Estimates potential returns
- **Risk Assessment**: Identifies potential risks
- **Optimization Suggestions**: Recommendations for improvement
- **Market Compatibility**: Checks strategy suitability

### **AI Recommendations**
- **Entry/Exit Points**: AI-suggested optimal timing
- **Risk Management**: Position sizing recommendations
- **Market Conditions**: Best market environments for strategy
- **Parameter Optimization**: Suggested parameter ranges
- **Backtesting Advice**: Historical testing recommendations

### **Strategy Management**
- **Strategy Library**: Save and organize strategies
- **Version Control**: Track strategy modifications
- **Performance Tracking**: Monitor strategy results
- **Comparison Tools**: Compare multiple strategies
- **Export Options**: Export analysis reports

---

## 🔄 **Integration Workflow**

### **Complete Trading Workflow**

#### **1. Setup Phase**
1. **Choose Theme**: Select preferred UI theme
2. **Add Credentials**: Set up Fyers and/or exchange credentials
3. **Select Mode**: Choose trading mode (backtest/paper/live)
4. **Upload Strategy**: Add PineScript strategy for AI analysis

#### **2. Strategy Development**
1. **AI Analysis**: Review AI recommendations for your strategy
2. **Backtest**: Test strategy with historical data
3. **Optimization**: Refine based on AI suggestions
4. **Paper Trading**: Test with live data simulation

#### **3. Live Deployment**
1. **Credential Verification**: Ensure live trading credentials work
2. **Final Testing**: Last validation in paper mode
3. **Live Launch**: Switch to live trading mode
4. **Monitoring**: Track performance and adjust

### **Multi-User Scenarios**
- **Team Trading**: Multiple users with individual credentials
- **Account Separation**: Each user's trades and data isolated
- **Shared Strategies**: AI analyses can be shared between users
- **Individual Preferences**: Each user has own theme and settings

---

## 🛠️ **Troubleshooting**

### **Common Issues & Solutions**

#### **Theme Issues**
- **Theme Not Switching**: Clear browser cache and localStorage
- **Missing Theme Elements**: Refresh page or restart browser
- **Animation Problems**: Disable browser extensions that might interfere

#### **Credential Issues**
- **Fyers Connection Failed**: Verify API credentials and trading PIN
- **TOTP Errors**: Ensure TOTP key is correctly entered
- **Exchange Authentication**: Check API key permissions and IP restrictions

#### **AI Strategy Issues**
- **Upload Failed**: Ensure file is valid PineScript (.pine extension)
- **Analysis Timeout**: Large strategies may take longer to process
- **Invalid Strategy**: AI will provide specific error messages

#### **General Issues**
- **Page Not Loading**: Check if both frontend and backend are running
- **API Errors**: Verify backend server is running on port 8000
- **Network Issues**: Check internet connection and firewall settings

### **Debug Information**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📞 **Support & Resources**

### **Documentation**
- **Installation Guide**: `/docs/INSTALLATION.md`
- **Deployment Guide**: `/docs/DEPLOYMENT_GUIDE_2025.md`
- **Feature Documentation**: `/docs/OCTOBER_2025_FEATURE_UPDATE.md`
- **API Documentation**: Available at `/docs` endpoint

### **Getting Help**
- **Error Messages**: Check console for detailed error information
- **Log Files**: Backend logs available in terminal output
- **API Testing**: Use `/docs` endpoint to test API functions
- **Browser DevTools**: Use F12 to inspect frontend issues

### **Best Practices**
1. **Always test strategies in backtest mode first**
2. **Use paper trading before live deployment**
3. **Keep credentials secure and never share**
4. **Regularly backup your strategy files**
5. **Monitor trades and performance regularly**
6. **Update API keys before they expire**

**🎉 Enjoy the enhanced AlgoProject experience with modern UI, secure credential management, and AI-powered strategy development!**