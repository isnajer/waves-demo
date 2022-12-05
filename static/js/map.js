// SOF:
fetch('/map')
anychart.onDocumentReady(function () {
  anychart.data.loadJsonFile("/map",
  function (data) {
      anychart.palettes
      .distinctColors()
      .items([
        '#fff59d',
        '#fbc02d',
        '#ff8f00',
        '#ef6c00',
        '#bbdefb',
        '#90caf9',
        '#64b5f6',
        '#42a5f5',
        '#1e88e5',
        '#1976d2',
        '#1565c0',
        '#01579b',
        '#0097a7',
        '#00838f'
      ]);

      var map = anychart.map();
      map.geoData(anychart.maps.world);

      var dataSet = anychart.data.set(data);
      // set the series
      var series = map.choropleth(dataSet);
    
      // disable labels
      series.labels(false);

      // set the container
      map.container('container');
      map.draw();

      // set map settings
      map
      .geoData('anychart.maps.world')
      .legend(false)
      .interactivity({ selectionMode: 'none' });

      map
        .title()
        .enabled(true)
        .fontSize(18)
        .padding(25, 25, 25, 25)
        .text('Sessions Around The World');

      map.background("rgba(255, 0, 0, 0");       
      // map
      //   .tooltip()
      //   .useHtml(true)
      //   .format(function () {
      //     var result;
      //     var value = '<span>';
      //     var description = '<br/><span>';
      //     if (this.value === '20000') {
      //       result = value + 'Never</span></strong>';
      //     } else result = value + this.value + '</span></strong>';

      //     if (
      //       getDescription(this.id) !== undefined &&
      //       getDescription(this.id) !== ''
      //     ) {
      //       result =
      //         result +
      //         description +
      //         getDescription(this.id) +
      //         '</span></strong>';
      //     }
      //     return result;
      //   });

      // create zoom controls
      var zoomController = anychart.ui.zoom();
      zoomController.render(map);

      // set container id for the chart
      map.container('container');
      // initiate chart drawing
      map.draw();
    }
  );
});