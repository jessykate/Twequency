function graph(div, friends) {
  console.log(friends);
  var r = Raphael(div);

  var percents = [];
  var frequencies = [];
  var labels = [];
  var x = [];
  for (var i=0; i< friends.length; i++) {
    labels[i] = friends[i][0];
    percents[i] = friends[i][1]['percent'];
    frequencies[i] = friends[i][1]['frequency'];
    x[i] = i*10;
    i++;
  }
  pie = r.g.linechart(1, 1, 400, 400, x, frequencies);
}