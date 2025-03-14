#!/usr/bin/env node

/**
 * Srcery Build Script
 *
 * This script builds the srcery.css CSS variable file included in package from
 * version 1.1.0 onward.
 *
 * Usage: node build.mjs
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import palette from './palette.json' with { type: 'json' };

// Get the directory name of the current module
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Function to generate CSS file from palette data
function generateCssFile(palette, outputPath) {
  try {
    let cssContent = ":root {\n";

    // Process primary colors
    Object.keys(palette.primary).forEach(colorName => {
      const color = palette.primary[colorName];
      cssContent += `  ${color.css}: ${color.hex};\n`;
    });

    // Process secondary colors
    Object.keys(palette.secondary).forEach(colorName => {
      const color = palette.secondary[colorName];
      cssContent += `  ${color.css}: ${color.hex};\n`;
    });

    cssContent += "}\n";

    // Write the CSS file
    fs.writeFileSync(outputPath, cssContent);
    console.log(`Successfully generated ${outputPath}`);

    return true;
  } catch (error) {
    console.error(`Error generating CSS file: ${error.message}`);
    return false;
  }
}

// Generate srcery.css file
const cssOutputPath = path.join(__dirname, 'srcery.css');
generateCssFile(palette, cssOutputPath);

