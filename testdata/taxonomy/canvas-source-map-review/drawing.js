export function paint(surface) {
  surface.fillRect(1, 2, 3, 4);
  surface.beginPath();
  surface.arc(5, 6, 7, 0, 2 * Math.PI);
  surface.fill();
}
