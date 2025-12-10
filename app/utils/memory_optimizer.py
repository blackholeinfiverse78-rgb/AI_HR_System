import gc
import psutil
import logging

logger = logging.getLogger(__name__)

class MemoryOptimizer:
    @staticmethod
    def optimize():
        """Force garbage collection and clear memory"""
        try:
            gc.collect()
            process = psutil.Process()
            mem_info = process.memory_info()
            logger.info(f"Memory optimized. Current usage: {mem_info.rss / 1024 / 1024:.2f} MB")
        except Exception as e:
            logger.error(f"Memory optimization failed: {e}")
    
    @staticmethod
    def get_memory_usage():
        """Get current memory usage percentage"""
        try:
            return psutil.virtual_memory().percent
        except:
            return 0
    
    @staticmethod
    def check_and_optimize(threshold=85):
        """Check memory and optimize if above threshold"""
        usage = MemoryOptimizer.get_memory_usage()
        if usage > threshold:
            logger.warning(f"High memory usage: {usage}%. Running optimization...")
            MemoryOptimizer.optimize()
            return True
        return False
