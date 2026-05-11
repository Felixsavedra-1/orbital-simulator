const puppeteer = require('puppeteer');
const GifEncoder = require('gif-encoder-2');
const Jimp = require('jimp');
const fs = require('fs');
const path = require('path');

const WIDTH = 800;
const HEIGHT = 450;
const FRAME_COUNT = 60;
const FRAME_DELAY = 100; // ms between frames

async function main() {
  console.log('Launching browser...');
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT });

  const htmlPath = path.resolve(__dirname, 'solar_system.html');
  await page.goto(`file://${htmlPath}`);

  // Wait for Three.js scene to initialize
  await new Promise(r => setTimeout(r, 2000));

  // Speed up the animation so all planets show visible movement
  await page.evaluate(() => {
    const slider = document.getElementById('speed');
    slider.value = 3;
    slider.dispatchEvent(new Event('input'));
  });

  console.log(`Capturing ${FRAME_COUNT} frames...`);
  const frames = [];
  for (let i = 0; i < FRAME_COUNT; i++) {
    const buf = await page.screenshot({ type: 'png' });
    frames.push(buf);
    process.stdout.write(`\r  frame ${i + 1}/${FRAME_COUNT}`);
    await new Promise(r => setTimeout(r, FRAME_DELAY));
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
