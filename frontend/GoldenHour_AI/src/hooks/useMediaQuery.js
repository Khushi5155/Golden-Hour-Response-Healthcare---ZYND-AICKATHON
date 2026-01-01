import { useState, useEffect } from 'react';

export function useMediaQuery(query) {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    // Check if window is defined (for SSR compatibility)
    if (typeof window === 'undefined') return false;

    const media = window.matchMedia(query);
    
    // Set initial value
    if (media.matches !== matches) {
      setMatches(media.matches);
    }

    // Define listener function
    const listener = (event) => {
      setMatches(event.matches);
    };

    // Use modern addEventListener instead of deprecated addListener
    if (media.addEventListener) {
      media.addEventListener('change', listener);
    } else {
      // Fallback for older browsers
      media.addListener(listener);
    }

    // Cleanup function
    return () => {
      if (media.removeEventListener) {
        media.removeEventListener('change', listener);
      } else {
        media.removeListener(listener);
      }
    };
  }, [query, matches]);

  return matches;
}
