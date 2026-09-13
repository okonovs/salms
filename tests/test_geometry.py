"""Numerical contract for area-driven, frame-corrected rectangle sampling."""
import math
import unittest


def rectangle(frame, aspect, low=4, high=18, ratio_low=.25, ratio_high=4, hold=4):
    index = frame // max(1, int(hold)) + 17
    def random(channel):
        value = math.sin(index * 12.9898 + channel * 78.233) * 43758.5453
        return value - math.floor(value)
    low, high = sorted(max(.001, min(.9, x / 100)) for x in (low, high))
    area = low + (high - low) * random(1)
    floor, ceiling = area * aspect / .9604, .9604 * aspect / area
    lo, hi = sorted(max(floor, min(ceiling, x)) for x in (ratio_low, ratio_high))
    ratio = math.exp(math.log(lo) + (math.log(hi) - math.log(lo)) * random(2))
    width, height = math.sqrt(area * ratio / aspect), math.sqrt(area * aspect / ratio)
    return width, height, area, ratio


class GeometryTests(unittest.TestCase):
    def test_area_and_containment_across_formats(self):
        for aspect in (16/9, 9/16, 1, 4):
            for bounds in ((4,18),(18,4),(.1,.1),(90,90)):
                for frame in range(400):
                    w,h,a,r = rectangle(frame, aspect, *bounds)
                    self.assertAlmostEqual(w*h, a)
                    self.assertAlmostEqual(w*aspect/h, r)
                    self.assertLessEqual(max(w,h), .980000001)

    def test_same_visual_shape_across_formats_when_it_fits(self):
        for frame in range(200):
            a=rectangle(frame,16/9,1,1)
            b=rectangle(frame,9/16,1,1)
            self.assertAlmostEqual(a[3],b[3])

    def test_defaults_generate_tall_and_wide_on_both_timeline_formats(self):
        for aspect in (16/9, 9/16):
            ratios = [rectangle(f, aspect)[3] for f in range(0, 400, 4)]
            self.assertGreater(sum(r < .5 for r in ratios), 10)
            self.assertGreater(sum(r > 2 for r in ratios), 10)

    def test_holds_and_both_orientations(self):
        values=[rectangle(f,16/9,1,1) for f in range(400)]
        for f,value in enumerate(values):
            self.assertEqual(value,values[f-f%4])
        self.assertTrue(any(v[3]<.5 for v in values))
        self.assertTrue(any(v[3]>2 for v in values))

if __name__ == '__main__':
    unittest.main()
