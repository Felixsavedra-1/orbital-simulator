const puppeteer = require('puppeteer');
const GifEncoder = require('gif-encoder-2');
const Jimp = require('jimp');
const fs = require('fs');
const path = require('path');

const WIDTH = 800;
const HEIGHT = 450;
const FRAME_DELAY = 100;        // ms between frames
const VIEWS = ['moon', 'solar', 'mars'];
const FRAMES_PER_VIEW = 20;     // ~2s per tab (incl. the camera ease-in)

async function main() {
  console.log('Launching browser...');
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await browser.newPage();
  // deviceScaleFactor: 2 makes the dashboard render at 1600×900 (via its
  // setPixelRatio cap) so we can supersample-downscale to 800×450 for crisp,
  // less-banded frames.
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 2 });

  const htmlPath = path.resolve(__dirname, 'solar_system.html');
  await page.goto(`file://${htmlPath}`);

  // Wait for Three.js scene to initialize
  await new Promise(r => setTimeout(r, 2000));

  // Calm, readable pace — 1.0× is the dashboard's natural default speed
  await page.evaluate(() => {
    const slider = document.getElementById('speed');
    slider.value = 1.0;
    slider.dispatchEvent(new Event('input'));
  });

  // Cycle the three tabs, capturing each view (the first frames of each
  // segment naturally include the dashboard's ~0.55s camera ease-in).
  const totalFrames = VIEWS.length * FRAMES_PER_VIEW;
  console.log(`Capturing ${totalFrames} frames across ${VIEWS.length} views...`);
  const frames = [];
  for (const view of VIEWS) {
    await page.evaluate(v => document.querySelector(`.tab[data-view="${v}"]`).click(), view);
    for (let i = 0; i < FRAMES_PER_VIEW; i++) {
      frames.push(await page.screenshot({ type: 'png' }));
      process.stdout.write(`\r  ${view}: frame ${i + 1}/${FRAMES_PER_VIEW}`);
      await new Promise(r => setTimeout(r, FRAME_DELAY));
    }
  }
  console.log();

  await browser.close();

  console.log('Encoding GIF...');
  const gif = new GifEncoder(WIDTH, HEIGHT, 'neuquant', true);
  gif.setDelay(FRAME_DELAY);
  gif.setRepeat(0); // loop forever
  gif.start();

  for (const buf of frames) {
    const img = await Jimp.read(buf);
    // Downscale the 1600×900 supersampled capture to the 800×450 output —
    // this is the anti-aliasing win and softens 256-color banding.
    img.resize(WIDTH, HEIGHT, Jimp.RESIZE_BICUBIC);
    gif.addFrame(img.bitmap.data);
  }

  gif.finish();

  const outPath = path.join(__dirname, 'preview.gif');
  const data = gif.out.getData();
  fs.writeFileSync(outPath, data);

  const kb = (data.length / 1024).toFixed(0);
  console.log(`Done! Saved preview.gif (${kb} KB)`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
