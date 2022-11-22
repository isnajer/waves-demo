fetch('/map')
anychart.onDocumentReady(function () {
    // The data used in this sample can be obtained from the CDN
    // https://cdn.anychart.com/samples/maps-choropleth/world-women-suffrage-map/data.json

    var data = [
        {'id': 'US', 'value': 5},
        {'id': 'CA', 'value': 2}
    ]
    // anychart.data.loadJsonFile(
    //   'https://cdn.anychart.com/samples/maps-choropleth/world-women-suffrage-map/data.json',
    //   function (data) {
    //     anychart.palettes
    //       .distinctColors()
    //       .items([
    //         '#fff59d',
    //         '#fbc02d',
    //         '#ff8f00',
    //         '#ef6c00',
    //         '#bbdefb',
    //         '#90caf9',
    //         '#64b5f6',
    //         '#42a5f5',
    //         '#1e88e5',
    //         '#1976d2',
    //         '#1565c0',
    //         '#01579b',
    //         '#0097a7',
    //         '#00838f'
    //       ]);
      
        var dataSet = anychart.data.set(data);

        var mapData = dataSet.mapAs({ description: 'description' });

        var map = anychart.map();

        // set map settings
        map
          .geoData('anychart.maps.world')
          .legend(false)
          .interactivity({ selectionMode: 'none' });

        map
          .title()
          .enabled(true)
          .fontSize(16)
          .padding(0, 0, 30, 0)
          .text('WAVES Around The World');

        var series = map.choropleth(mapData);
        series.geoIdField('iso_a2').labels(false);
        series.hovered().fill('#455a64');
        var scale = anychart.scales.ordinalColor([
          { less: 1 },
          { from: 1, to: 5 },
          { from: 5, to: 10 },
          { from: 10, to: 15 },
          { from: 15, to: 20 },
          { from: 20, to: 25 },
          { from: 25, to: 30 },
          { greater: 30 }
        ]);

        scale.colors([
          '#42a5f5',
          '#64b5f6',
          '#90caf9',
          '#ffa726',
          '#fb8c00',
          '#f57c00',
          '#ef6c00',
          '#e65100'
        ]);
        series.colorScale(scale);

        var colorRange = map.colorRange();
        colorRange
          .enabled(true)
          .padding([20, 0, 0, 0])
          .colorLineSize(5)
          .marker({ size: 7 });
        colorRange
          .ticks()
          .enabled(true)
          .stroke('3 #ffffff')
          .position('center')
          .length(20);
        colorRange
          .labels()
          .fontSize(10)
          .padding(0, 0, 0, 5)
          .format(function () {
            var range = this.colorRange;
            var name;
            if (isFinite(range.start + range.end)) {
              name = range.start + ' - ' + range.end;
            } else if (isFinite(range.start)) {
              name = 'Greater than ' + range.start;
            } else {
              name = 'Fewer than ' + range.end;
            }
            return name;
          });

        map
          .tooltip()
          .useHtml(true)
          .format(function () {
            var result;
            var value = '<span>';
            var description = '<br/><span>';
            if (this.value === '20000') {
              result = value + 'Never</span></strong>';
            } else result = value + this.value + '</span></strong>';

            if (
              getDescription(this.id) !== undefined &&
              getDescription(this.id) !== ''
            ) {
              result =
                result +
                description +
                getDescription(this.id) +
                '</span></strong>';
            }
            return result;
          });

        // create zoom controls
        var zoomController = anychart.ui.zoom();
        zoomController.render(map);

        // set container id for the chart
        map.container('container');
        // initiate chart drawing
        map.draw();

        function getDescription(id) {
          for (var i = 0; i < data.length; i++) {
            if (data[i].id === id) return data[i].description;
          }
        }
      }
    );
