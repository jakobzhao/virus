# Embedding this map a web page

## A universal approach (If the display area is narrower than 1026px)

please insert the following code snippet to your html page.

```html
<object type="text/html" style="transform-origin: top left; -moz-transform: scale(0.5);  -webkit-transform: scale(0.5); transform: scale(0.5); width: 1800px; height: 1200px;" data="https://hgis.uw.edu/virus/">
  </object>
```

Then, you need to update all the three scale number to a viusally appropriate number. Please make sure all the three numbers are equal. For example, you can change the number to `0.75` or `0.8`.

If you want to adjust the width/height ratio, please just change the height `1200px`. For example, if you want the w/h ratio is 5/3, then please change the height to `1080px`.

If you want to see how it works, you can visit http://hgis.uw.edu/virus/embed2.html

## If the display area is wider than 1026 px

please insert the following code snippet to your html page.


```html
<object type="text/html" width="1020" height="800" data="https://hgis.uw.edu/virus/">
</object>
```

You can just change the width and height to adjust the size and view port shape. If you want to see how it works, you can visit http://hgis.uw.edu/virus/embed.html
