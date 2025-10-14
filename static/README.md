# Static Assets - Everforest Theme

This directory contains static assets for the lovelyRSS application with a beautiful Everforest-inspired minimal theme.

## Theme Overview

The current styling implements a clean, minimal design inspired by the Everforest color scheme:

- **Light Theme**: Warm, natural colors with soft greens and earth tones
- **Dark Theme**: Automatic dark mode support with forest-inspired dark palette
- **Typography**: Inter font for UI elements, Merriweather for reading content
- **Responsive**: Mobile-first design with smooth transitions

## Color Palette

### Light Theme
- Background: `#fffefb` (warm white)
- Surface: `#f4f1ed` (soft beige)
- Primary Text: `#5c6a72` (slate gray)
- Accent: `#8da101` (forest green)

### Dark Theme
- Background: `#2d353b` (dark forest)
- Surface: `#343f44` (charcoal)
- Primary Text: `#d3c6aa` (warm cream)
- Accent: `#a7c080` (light forest green)

## Files

- `custom.css` - Main theme stylesheet with Everforest colors and minimal styling
- `favicon.ico` - Site favicon (add your own)
- `logo.png` - Site logo (optional)

## Customization

### Adding a Custom Favicon

1. Create or find a 32x32 pixel ICO file
2. Name it `favicon.ico`
3. Place it in this directory

### Modifying the Theme

The theme uses CSS custom properties (variables) for easy customization. Key variables include:

```css
:root {
  --accent-primary: #8da101;     /* Primary accent color */
  --text-primary: #5c6a72;       /* Main text color */
  --bg-main: #fffefb;            /* Background color */
  --border-light: #e8e5e0;       /* Border color */
}
```

### Theme Features

- **Minimal Design**: Clean, distraction-free reading experience
- **Everforest Colors**: Warm, natural color palette inspired by forest themes
- **Smooth Animations**: Subtle hover effects and transitions
- **Typography**: Optimized font choices for excellent readability
- **Accessibility**: Proper focus states and contrast ratios
- **Responsive**: Mobile-optimized with touch-friendly interactions

## Browser Support

The theme uses modern CSS features and works best in:
- Chrome/Chromium 88+
- Firefox 85+
- Safari 14+
- Edge 88+

## Contributing

When modifying the theme:
1. Maintain the existing CSS custom property structure
2. Test in both light and dark modes
3. Ensure mobile responsiveness
4. Verify accessibility standards