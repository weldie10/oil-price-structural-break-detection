# Dashboard Screenshots

This directory should contain screenshots of the dashboard demonstrating all features.

## Required Screenshots

1. **dashboard-desktop.png** - Full desktop view showing:
   - Price chart with event markers
   - Filters panel
   - Statistics panel
   - Event list

2. **dashboard-mobile.png** - Mobile responsive view showing:
   - Single column layout
   - Touch-optimized interface
   - Responsive filters

3. **dashboard-filters.png** - Filters panel showing:
   - Date range inputs
   - Event type dropdown
   - Impact type dropdown
   - Severity dropdown
   - Clear filters button

4. **dashboard-events.png** - Event highlighting on chart showing:
   - Vertical dashed lines for events
   - Diamond markers at event prices
   - Color-coded events by severity
   - Hover tooltips

## How to Take Screenshots

### Desktop Screenshots

1. Start both backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. Use browser developer tools (F12) to:
   - Set viewport to 1920x1080 for desktop
   - Take screenshot using browser's screenshot tool or a tool like:
     - Chrome: Use "Capture screenshot" in DevTools
     - Firefox: Use "Take a screenshot" in DevTools
     - Or use a tool like Greenshot, Snagit, or Snipping Tool

### Mobile Screenshots

1. Open `http://localhost:3000` in your browser
2. Use browser developer tools (F12) to:
   - Toggle device toolbar (Ctrl+Shift+M)
   - Select a mobile device (e.g., iPhone 12, Pixel 5)
   - Take screenshot

### Alternative: Using Browser Automation

You can use tools like:
- **Playwright**: Automated browser screenshots
- **Puppeteer**: Headless Chrome screenshots
- **Selenium**: Cross-browser screenshots

Example Playwright script:
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:3000');
  await page.screenshot({ path: 'dashboard-desktop.png', fullPage: true });
  await browser.close();
})();
```

## Screenshot Specifications

- **Format**: PNG (preferred) or JPG
- **Resolution**: 
  - Desktop: 1920x1080 or higher
  - Mobile: Device-specific (e.g., 375x667 for iPhone)
- **File Size**: Keep under 2MB per image
- **Naming**: Use descriptive names as listed above

## Notes

- Ensure all features are visible in screenshots
- Use a clean browser window (no extensions visible)
- Include examples of filtered data
- Show event markers clearly on the chart
- Demonstrate responsive behavior in mobile screenshots
