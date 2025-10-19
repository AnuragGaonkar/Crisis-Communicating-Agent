from ddgs import DDGS  # FIXED: Changed from duckduckgo_search
import time


class WebSearchAgent:
    def __init__(self):
        self.ddgs = DDGS()
        
    def search(self, query, num_results=5):
        """Simple reliable search"""
        try:
            results = []
            search_results = self.ddgs.text(query, max_results=num_results)
            
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'snippet': result.get('body', ''),
                    'source': result.get('href', '').split('/')[2] if result.get('href') else 'Unknown'
                })
            
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def verify_claim(self, claim):
        """Simplified verification that ACTUALLY WORKS"""
        
        print(f"Searching for: {claim}")
        
        # Try multiple simpler queries
        queries = [
            claim,  # Original query
            f"{claim} facts",
            f"{claim} information"
        ]
        
        all_results = []
        
        for query in queries:
            try:
                results = self.search(query, num_results=5)
                print(f"  Query '{query[:50]}...' returned {len(results)} results")
                all_results.extend(results)
                time.sleep(0.5)
                
                if len(all_results) >= 5:
                    break
            except:
                continue
        
        # Remove duplicates
        seen_urls = set()
        unique_results = []
        for r in all_results:
            if r['url'] not in seen_urls:
                seen_urls.add(r['url'])
                # Skip obviously bad domains
                if not any(bad in r['url'].lower() for bad in ['support.google', 'login', 'signin', 'd-id.com']):
                    unique_results.append(r)
        
        print(f"  Final unique results: {len(unique_results)}")
        
        if not unique_results:
            return {
                'verified': False,
                'confidence': 0.0,
                'sources': [],
                'verified_sources': []
            }
        
        # Check for trusted sources
        trusted = ['wikipedia', 'britannica', 'nasa.gov', 'gov', 'edu', 'bbc', 'reuters',
                  'indianexpress', 'thehindu', 'ndtv', 'timesofindia', 'who.int', 'un.org']
        
        verified_sources = [r for r in unique_results if any(t in r['source'].lower() for t in trusted)]
        
        return {
            'verified': len(verified_sources) > 0,
            'confidence': len(verified_sources) / len(unique_results) if unique_results else 0,
            'sources': unique_results[:5],
            'verified_sources': verified_sources
        }
