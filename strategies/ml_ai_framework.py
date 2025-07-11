"""
AlgoProject - Advanced ML/AI Trading Framework
Comprehensive machine learning and artificial intelligence-based trading strategies
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import TimeSeriesSplit
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import classification_report, accuracy_score
    from joblib import dump, load
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️  Scikit-learn not available. Install with: pip install scikit-learn joblib")

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("⚠️  Scipy not available. Install with: pip install scipy")


class MLAITradingFramework:
    """
    Advanced ML/AI Trading Framework with ensemble models and smart money tracking
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or self._default_config()
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        self.smart_money_tracker = SmartMoneyTracker()
        self.institutional_analyzer = InstitutionalAnalyzer()
        self.prediction_history = []
        self.confidence_threshold = 0.6
        
    def _default_config(self) -> Dict:
        return {
            'models': {
                'rf': {'n_estimators': 100, 'max_depth': 10, 'random_state': 42},
                'gb': {'n_estimators': 100, 'max_depth': 6, 'random_state': 42},
                'lr': {'random_state': 42, 'max_iter': 1000}
            },
            'features': {
                'technical': True,
                'volume': True,
                'volatility': True,
                'momentum': True,
                'smart_money': True,
                'institutional': True
            },
            'lookback_period': 60,
            'prediction_horizon': 1,
            'train_test_split': 0.8
        }
    
    def generate_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate comprehensive feature set for ML models
        """
        features = pd.DataFrame(index=data.index)
        
        # Price features
        features['price'] = data['close']
        features['price_change'] = data['close'].pct_change()
        features['price_change_abs'] = features['price_change'].abs()
        
        # Technical indicators
        if self.config['features']['technical']:
            features = self._add_technical_features(features, data)
        
        # Volume features
        if self.config['features']['volume']:
            features = self._add_volume_features(features, data)
        
        # Volatility features
        if self.config['features']['volatility']:
            features = self._add_volatility_features(features, data)
        
        # Momentum features
        if self.config['features']['momentum']:
            features = self._add_momentum_features(features, data)
        
        # Smart money features
        if self.config['features']['smart_money']:
            features = self._add_smart_money_features(features, data)
        
        # Institutional features
        if self.config['features']['institutional']:
            features = self._add_institutional_features(features, data)
        
        return features.fillna(0)
    
    def _add_technical_features(self, features: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        """Add technical analysis features"""
        # Moving averages
        for period in [5, 10, 20, 50]:
            features[f'ma_{period}'] = data['close'].rolling(period).mean()
            features[f'ma_{period}_ratio'] = data['close'] / features[f'ma_{period}']
        
        # RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        features['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        ema_12 = data['close'].ewm(span=12).mean()
        ema_26 = data['close'].ewm(span=26).mean()
        features['macd'] = ema_12 - ema_26
        features['macd_signal'] = features['macd'].ewm(span=9).mean()
        features['macd_histogram'] = features['macd'] - features['macd_signal']
        
        # Bollinger Bands
        sma_20 = data['close'].rolling(20).mean()
        std_20 = data['close'].rolling(20).std()
        features['bb_upper'] = sma_20 + (std_20 * 2)
        features['bb_lower'] = sma_20 - (std_20 * 2)
        features['bb_position'] = (data['close'] - features['bb_lower']) / (features['bb_upper'] - features['bb_lower'])
        
        return features
    
    def _add_volume_features(self, features: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        """Add volume-based features"""
        features['volume'] = data['volume']
        features['volume_ma'] = data['volume'].rolling(20).mean()
        features['volume_ratio'] = data['volume'] / features['volume_ma']
        features['volume_price_trend'] = data['volume'] * (data['close'] - data['open'])
        
        # On-Balance Volume (OBV)
        obv = []
        obv_value = 0
        for i in range(len(data)):
            if i == 0:
                obv.append(data['volume'].iloc[i])
            else:
                if data['close'].iloc[i] > data['close'].iloc[i-1]:
                    obv_value += data['volume'].iloc[i]
                elif data['close'].iloc[i] < data['close'].iloc[i-1]:
                    obv_value -= data['volume'].iloc[i]
                obv.append(obv_value)
        features['obv'] = obv
        
        return features
    
    def _add_volatility_features(self, features: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        """Add volatility-based features"""
        features['high_low_ratio'] = data['high'] / data['low']
        features['true_range'] = np.maximum(
            data['high'] - data['low'],
            np.maximum(
                abs(data['high'] - data['close'].shift(1)),
                abs(data['low'] - data['close'].shift(1))
            )
        )
        features['atr'] = features['true_range'].rolling(14).mean()
        features['volatility'] = data['close'].pct_change().rolling(20).std()
        
        return features
    
    def _add_momentum_features(self, features: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        """Add momentum-based features"""
        # Rate of Change
        for period in [5, 10, 20]:
            features[f'roc_{period}'] = data['close'].pct_change(period)
        
        # Stochastic Oscillator
        low_14 = data['low'].rolling(14).min()
        high_14 = data['high'].rolling(14).max()
        features['stoch_k'] = 100 * (data['close'] - low_14) / (high_14 - low_14)
        features['stoch_d'] = features['stoch_k'].rolling(3).mean()
        
        # Williams %R
        features['williams_r'] = -100 * (high_14 - data['close']) / (high_14 - low_14)
        
        return features
    
    def _add_smart_money_features(self, features: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        """Add smart money tracking features"""
        smart_money_data = self.smart_money_tracker.analyze(data)
        features['smart_money_index'] = smart_money_data['smart_money_index']
        features['accumulation_distribution'] = smart_money_data['accumulation_distribution']
        features['money_flow_index'] = smart_money_data['money_flow_index']
        
        return features
    
    def _add_institutional_features(self, features: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        """Add institutional analysis features"""
        institutional_data = self.institutional_analyzer.analyze(data)
        features['institutional_flow'] = institutional_data['institutional_flow']
        features['large_order_imbalance'] = institutional_data['large_order_imbalance']
        features['institutional_sentiment'] = institutional_data['institutional_sentiment']
        
        return features
    
    def create_target_variable(self, data: pd.DataFrame, method: str = 'next_return') -> pd.Series:
        """
        Create target variable for ML models
        """
        if method == 'next_return':
            # Predict next period return direction
            next_return = data['close'].pct_change().shift(-1)
            return (next_return > 0).astype(int)
        elif method == 'multi_class':
            # Multi-class classification: Strong Up, Up, Neutral, Down, Strong Down
            next_return = data['close'].pct_change().shift(-1)
            conditions = [
                next_return > 0.02,  # Strong Up
                (next_return > 0) & (next_return <= 0.02),  # Up
                (next_return >= -0.01) & (next_return <= 0.01),  # Neutral
                (next_return < 0) & (next_return >= -0.02),  # Down
                next_return < -0.02  # Strong Down
            ]
            choices = [2, 1, 0, -1, -2]
            return pd.Series(np.select(conditions, choices, default=0), index=data.index)
        
        return pd.Series(index=data.index, dtype=int)
    
    def train_models(self, data: pd.DataFrame) -> Dict:
        """
        Train ensemble of ML models
        """
        if not SKLEARN_AVAILABLE:
            print("❌ Scikit-learn not available. Cannot train ML models.")
            return {}
        
        # Generate features and target
        features = self.generate_features(data)
        target = self.create_target_variable(data)
        
        # Remove NaN values
        mask = ~(features.isna().any(axis=1) | target.isna())
        features = features[mask]
        target = target[mask]
        
        if len(features) < 100:
            print("❌ Insufficient data for training ML models.")
            return {}
        
        # Split data
        split_idx = int(len(features) * self.config['train_test_split'])
        X_train, X_test = features.iloc[:split_idx], features.iloc[split_idx:]
        y_train, y_test = target.iloc[:split_idx], target.iloc[split_idx:]
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        self.scalers['main'] = scaler
        
        # Train models
        models = {}
        results = {}
        
        # Random Forest
        if 'rf' in self.config['models']:
            rf_model = RandomForestClassifier(**self.config['models']['rf'])
            rf_model.fit(X_train_scaled, y_train)
            rf_pred = rf_model.predict(X_test_scaled)
            rf_accuracy = accuracy_score(y_test, rf_pred)
            
            models['rf'] = rf_model
            results['rf'] = {'accuracy': rf_accuracy, 'predictions': rf_pred}
            
            # Feature importance
            feature_importance = pd.DataFrame({
                'feature': X_train.columns,
                'importance': rf_model.feature_importances_
            }).sort_values('importance', ascending=False)
            self.feature_importance['rf'] = feature_importance
        
        # Gradient Boosting
        if 'gb' in self.config['models']:
            gb_model = GradientBoostingClassifier(**self.config['models']['gb'])
            gb_model.fit(X_train_scaled, y_train)
            gb_pred = gb_model.predict(X_test_scaled)
            gb_accuracy = accuracy_score(y_test, gb_pred)
            
            models['gb'] = gb_model
            results['gb'] = {'accuracy': gb_accuracy, 'predictions': gb_pred}
            
            # Feature importance
            feature_importance = pd.DataFrame({
                'feature': X_train.columns,
                'importance': gb_model.feature_importances_
            }).sort_values('importance', ascending=False)
            self.feature_importance['gb'] = feature_importance
        
        # Logistic Regression
        if 'lr' in self.config['models']:
            lr_model = LogisticRegression(**self.config['models']['lr'])
            lr_model.fit(X_train_scaled, y_train)
            lr_pred = lr_model.predict(X_test_scaled)
            lr_accuracy = accuracy_score(y_test, lr_pred)
            
            models['lr'] = lr_model
            results['lr'] = {'accuracy': lr_accuracy, 'predictions': lr_pred}
        
        self.models = models
        
        # Ensemble prediction
        if len(models) > 1:
            ensemble_pred = []
            for i in range(len(X_test)):
                votes = [results[model]['predictions'][i] for model in models.keys()]
                ensemble_pred.append(max(set(votes), key=votes.count))
            
            ensemble_accuracy = accuracy_score(y_test, ensemble_pred)
            results['ensemble'] = {'accuracy': ensemble_accuracy, 'predictions': ensemble_pred}
        
        return results
    
    def predict(self, data: pd.DataFrame) -> Dict:
        """
        Make ensemble prediction
        """
        if not self.models:
            return {'signal': 0, 'confidence': 0, 'individual_predictions': {}}
        
        # Generate features
        features = self.generate_features(data)
        
        # Use only the last row for prediction
        if len(features) == 0:
            return {'signal': 0, 'confidence': 0, 'individual_predictions': {}}
        
        last_features = features.iloc[-1:].fillna(0)
        
        # Scale features
        if 'main' in self.scalers:
            last_features_scaled = self.scalers['main'].transform(last_features)
        else:
            last_features_scaled = last_features.values
        
        # Get predictions from all models
        predictions = {}
        probabilities = {}
        
        for model_name, model in self.models.items():
            try:
                pred = model.predict(last_features_scaled)[0]
                predictions[model_name] = pred
                
                # Get probability if available
                if hasattr(model, 'predict_proba'):
                    proba = model.predict_proba(last_features_scaled)[0]
                    probabilities[model_name] = max(proba)
                else:
                    probabilities[model_name] = 0.6  # Default confidence
            except Exception as e:
                print(f"⚠️  Error predicting with {model_name}: {e}")
                predictions[model_name] = 0
                probabilities[model_name] = 0
        
        # Ensemble prediction
        if predictions:
            # Weighted voting based on confidence
            weighted_sum = sum(pred * prob for pred, prob in zip(predictions.values(), probabilities.values()))
            total_weight = sum(probabilities.values())
            
            if total_weight > 0:
                ensemble_signal = 1 if weighted_sum / total_weight > 0.5 else 0
                ensemble_confidence = total_weight / len(predictions)
            else:
                ensemble_signal = 0
                ensemble_confidence = 0
        else:
            ensemble_signal = 0
            ensemble_confidence = 0
        
        # Convert to trading signal
        if ensemble_signal == 1 and ensemble_confidence > self.confidence_threshold:
            final_signal = 1  # Buy
        elif ensemble_signal == 0 and ensemble_confidence > self.confidence_threshold:
            final_signal = -1  # Sell
        else:
            final_signal = 0  # Hold
        
        result = {
            'signal': final_signal,
            'confidence': ensemble_confidence,
            'individual_predictions': predictions,
            'individual_probabilities': probabilities
        }
        
        self.prediction_history.append(result)
        
        return result
    
    def generate_signals(self, data: pd.DataFrame) -> List[Dict]:
        """
        Generate signals wrapper for compatibility
        """
        try:
            prediction = self.predict(data)
            if prediction.get('signal', 0) != 0:
                return [{
                    'signal_type': 'BUY' if prediction['signal'] > 0 else 'SELL',
                    'strategy': 'ml_ai_framework',
                    'confidence': prediction.get('confidence', 0),
                    'predictions': prediction.get('individual_predictions', {}),
                    'entry_price': data['close'].iloc[-1],
                    'timestamp': datetime.now()
                }]
            else:
                return []
        except Exception as e:
            print(f"⚠️  Error in generate_signals: {e}")
            return []
    
    def get_feature_importance(self) -> Dict:
        """Get feature importance from trained models"""
        return self.feature_importance
    
    def save_models(self, filepath: str):
        """Save trained models"""
        if not self.models:
            print("❌ No models to save")
            return
        
        try:
            model_data = {
                'models': self.models,
                'scalers': self.scalers,
                'config': self.config,
                'feature_importance': self.feature_importance
            }
            dump(model_data, filepath)
            print(f"✅ Models saved to {filepath}")
        except Exception as e:
            print(f"❌ Error saving models: {e}")
    
    def load_models(self, filepath: str):
        """Load trained models"""
        try:
            model_data = load(filepath)
            self.models = model_data['models']
            self.scalers = model_data['scalers']
            self.config = model_data['config']
            self.feature_importance = model_data['feature_importance']
            print(f"✅ Models loaded from {filepath}")
        except Exception as e:
            print(f"❌ Error loading models: {e}")


class SmartMoneyTracker:
    """
    Smart Money Tracking and Analysis
    """
    
    def analyze(self, data: pd.DataFrame) -> Dict:
        """
        Analyze smart money activity
        """
        result = {
            'smart_money_index': pd.Series(index=data.index, dtype=float),
            'accumulation_distribution': pd.Series(index=data.index, dtype=float),
            'money_flow_index': pd.Series(index=data.index, dtype=float)
        }
        
        try:
            # Smart Money Index (SMI)
            # Based on volume and price action
            volume_ma = data['volume'].rolling(20).mean()
            price_change = data['close'].pct_change()
            
            # Smart money tends to accumulate on down days with high volume
            smart_money_signals = []
            for i in range(len(data)):
                if i < 20:  # Not enough data
                    smart_money_signals.append(0)
                else:
                    volume_ratio = data['volume'].iloc[i] / volume_ma.iloc[i]
                    price_change_val = price_change.iloc[i]
                    
                    # Smart money accumulation: high volume on down days
                    if volume_ratio > 1.5 and price_change_val < -0.01:
                        smart_money_signals.append(1)
                    # Smart money distribution: high volume on up days
                    elif volume_ratio > 1.5 and price_change_val > 0.01:
                        smart_money_signals.append(-1)
                    else:
                        smart_money_signals.append(0)
            
            result['smart_money_index'] = pd.Series(smart_money_signals, index=data.index)
            
            # Accumulation/Distribution Line
            ad_line = []
            ad_value = 0
            for i in range(len(data)):
                if data['high'].iloc[i] != data['low'].iloc[i]:
                    money_flow_multiplier = ((data['close'].iloc[i] - data['low'].iloc[i]) - 
                                           (data['high'].iloc[i] - data['close'].iloc[i])) / (data['high'].iloc[i] - data['low'].iloc[i])
                    money_flow_volume = money_flow_multiplier * data['volume'].iloc[i]
                    ad_value += money_flow_volume
                ad_line.append(ad_value)
            
            result['accumulation_distribution'] = pd.Series(ad_line, index=data.index)
            
            # Money Flow Index
            typical_price = (data['high'] + data['low'] + data['close']) / 3
            money_flow = typical_price * data['volume']
            
            positive_flow = []
            negative_flow = []
            
            for i in range(1, len(data)):
                if typical_price.iloc[i] > typical_price.iloc[i-1]:
                    positive_flow.append(money_flow.iloc[i])
                    negative_flow.append(0)
                elif typical_price.iloc[i] < typical_price.iloc[i-1]:
                    positive_flow.append(0)
                    negative_flow.append(money_flow.iloc[i])
                else:
                    positive_flow.append(0)
                    negative_flow.append(0)
            
            # Add first value as 0
            positive_flow.insert(0, 0)
            negative_flow.insert(0, 0)
            
            positive_flow_series = pd.Series(positive_flow, index=data.index)
            negative_flow_series = pd.Series(negative_flow, index=data.index)
            
            positive_flow_14 = positive_flow_series.rolling(14).sum()
            negative_flow_14 = negative_flow_series.rolling(14).sum()
            
            money_flow_ratio = positive_flow_14 / negative_flow_14
            mfi = 100 - (100 / (1 + money_flow_ratio))
            
            result['money_flow_index'] = mfi.fillna(50)
            
        except Exception as e:
            print(f"⚠️  Error in smart money analysis: {e}")
            # Return default values
            result['smart_money_index'] = pd.Series([0] * len(data), index=data.index)
            result['accumulation_distribution'] = pd.Series([0] * len(data), index=data.index)
            result['money_flow_index'] = pd.Series([50] * len(data), index=data.index)
        
        return result


class InstitutionalAnalyzer:
    """
    Institutional Activity Analysis
    """
    
    def analyze(self, data: pd.DataFrame) -> Dict:
        """
        Analyze institutional trading activity
        """
        result = {
            'institutional_flow': pd.Series(index=data.index, dtype=float),
            'large_order_imbalance': pd.Series(index=data.index, dtype=float),
            'institutional_sentiment': pd.Series(index=data.index, dtype=float)
        }
        
        try:
            # Institutional Flow based on volume and price patterns
            volume_ma = data['volume'].rolling(20).mean()
            volume_std = data['volume'].rolling(20).std()
            
            # Detect large volume spikes (potential institutional activity)
            large_volume_threshold = volume_ma + (2 * volume_std)
            institutional_flow = []
            
            for i in range(len(data)):
                if i < 20:
                    institutional_flow.append(0)
                else:
                    current_volume = data['volume'].iloc[i]
                    threshold = large_volume_threshold.iloc[i]
                    
                    if current_volume > threshold:
                        # Determine direction based on price action
                        price_change = (data['close'].iloc[i] - data['open'].iloc[i]) / data['open'].iloc[i]
                        if price_change > 0:
                            institutional_flow.append(1)  # Institutional buying
                        else:
                            institutional_flow.append(-1)  # Institutional selling
                    else:
                        institutional_flow.append(0)
            
            result['institutional_flow'] = pd.Series(institutional_flow, index=data.index)
            
            # Large Order Imbalance
            # Based on volume-weighted price analysis
            vwap = (data['volume'] * (data['high'] + data['low'] + data['close']) / 3).cumsum() / data['volume'].cumsum()
            
            large_order_imbalance = []
            for i in range(len(data)):
                if i < 10:
                    large_order_imbalance.append(0)
                else:
                    price_vs_vwap = (data['close'].iloc[i] - vwap.iloc[i]) / vwap.iloc[i]
                    volume_ratio = data['volume'].iloc[i] / volume_ma.iloc[i] if volume_ma.iloc[i] > 0 else 1
                    
                    # Large order imbalance score
                    imbalance_score = price_vs_vwap * volume_ratio
                    large_order_imbalance.append(imbalance_score)
            
            result['large_order_imbalance'] = pd.Series(large_order_imbalance, index=data.index)
            
            # Institutional Sentiment
            # Combine multiple factors
            institutional_sentiment = []
            for i in range(len(data)):
                if i < 20:
                    institutional_sentiment.append(0)
                else:
                    # Factors: institutional flow, volume, price momentum
                    flow_factor = institutional_flow[i]
                    volume_factor = (data['volume'].iloc[i] / volume_ma.iloc[i] - 1) if volume_ma.iloc[i] > 0 else 0
                    
                    # Price momentum over last 5 days
                    momentum_factor = (data['close'].iloc[i] / data['close'].iloc[i-5] - 1) if i >= 5 else 0
                    
                    # Combined sentiment score
                    sentiment = (flow_factor * 0.5 + volume_factor * 0.3 + momentum_factor * 0.2)
                    institutional_sentiment.append(sentiment)
            
            result['institutional_sentiment'] = pd.Series(institutional_sentiment, index=data.index)
            
        except Exception as e:
            print(f"⚠️  Error in institutional analysis: {e}")
            # Return default values
            result['institutional_flow'] = pd.Series([0] * len(data), index=data.index)
            result['large_order_imbalance'] = pd.Series([0] * len(data), index=data.index)
            result['institutional_sentiment'] = pd.Series([0] * len(data), index=data.index)
        
        return result


# Example usage and testing
if __name__ == "__main__":
    # Test the ML/AI Framework
    print("🧠 Testing ML/AI Trading Framework")
    
    # Create sample data
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    
    sample_data = pd.DataFrame({
        'open': 100 + np.random.randn(len(dates)).cumsum() * 0.5,
        'high': 101 + np.random.randn(len(dates)).cumsum() * 0.5,
        'low': 99 + np.random.randn(len(dates)).cumsum() * 0.5,
        'close': 100 + np.random.randn(len(dates)).cumsum() * 0.5,
        'volume': np.random.randint(1000, 10000, len(dates))
    }, index=dates)
    
    # Ensure high >= low and realistic OHLC relationships
    sample_data['high'] = np.maximum(sample_data[['open', 'close']].max(axis=1), sample_data['high'])
    sample_data['low'] = np.minimum(sample_data[['open', 'close']].min(axis=1), sample_data['low'])
    
    # Initialize framework
    framework = MLAITradingFramework()
    
    # Train models
    print("📈 Training ML models...")
    training_results = framework.train_models(sample_data)
    
    if training_results:
        print("✅ Model training completed")
        for model_name, results in training_results.items():
            print(f"  {model_name}: {results['accuracy']:.3f} accuracy")
    else:
        print("❌ Model training failed")
    
    # Make predictions
    print("\n🔮 Making predictions...")
    prediction = framework.predict(sample_data)
    print(f"Signal: {prediction['signal']}")
    print(f"Confidence: {prediction['confidence']:.3f}")
    print(f"Individual predictions: {prediction['individual_predictions']}")
    
    # Feature importance
    feature_importance = framework.get_feature_importance()
    if feature_importance:
        print("\n📊 Top 10 Most Important Features:")
        for model_name, importance_df in feature_importance.items():
            print(f"\n{model_name.upper()} Model:")
            print(importance_df.head(10).to_string(index=False))
    
    print("\n🎯 ML/AI Framework test completed!")
