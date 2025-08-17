#!/usr/bin/env python3
"""
Generate summary table from existing batch runner results
"""
import sys
import os
from pathlib import Path

# Add the scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))
os.chdir(scripts_dir)

def test_summary_generation():
    """Test the summary generation with existing results"""
    
    print("📊 TESTING SUMMARY GENERATION")
    print("=" * 50)
    
    try:
        # Import the new function
        from batch_runner import generate_comprehensive_summary, discover_strategies, get_available_timeframes
        
        # Get strategies and timeframes
        strategies = discover_strategies()
        timeframes = get_available_timeframes()
        symbols = ['BTC/USDT']
        
        # Point to the existing results
        output_dir = "../output/comprehensive_analysis_20250715_235752"
        
        print(f"📁 Using existing results from: {output_dir}")
        print(f"🧪 Strategies: {len(strategies)}")
        print(f"⏰ Timeframes: {len(timeframes)}")
        
        # Generate summary
        success = generate_comprehensive_summary(
            output_dir=output_dir,
            symbols=symbols,
            strategies=strategies,
            timeframes=timeframes
        )
        
        if success:
            print("\n✅ Summary generation completed!")
        else:
            print("\n❌ Summary generation failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_summary_generation()
