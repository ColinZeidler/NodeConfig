$( document ).ready(function() {
var svg = d3.select("svg");
var width = +svg.attr("width");
var height = +svg.attr("height");

var sim = d3.forceSimulation()
	.force("link", d3.forceLink().id(function(d) { return d.id; }))
	.force("charge", d3.forceManyBody())
	.force("center", d3.forceCenter(width/2, height/2));

d3.json("/nodes", function(error, n) {
	d3.json("/topology", function(error, t) {
	console.log(n)
	console.log(t)
	var link = svg.append("g")
		.attr("class", "links")
		.selectAll("line")
		.data(t)
		.enter().append("line")
			.attr("class", "link");

	var node = svg.append("g")
		.attr("class", "nodes")
		.selectAll(".node")
		.data(n)
		.enter().append("g")
			.attr("class", "node")

		node.append("circle")
			.attr("r", 7)
			.on("click", node_click).text(function(d) { return d.name; });
		node.append("text")
			.attr("dx", 10)
			.attr("dy", ".35em")
			.text(function(d) { return d.name; });

		sim.nodes(n).on("tick", tick);
		sim.force("link").links(t).distance(75);

	function tick() {
		d3.selectAll("circle")
			.attr("cx", function(d) { return d.x; })
			.attr("cy", function(d) { return d.y; });
		d3.selectAll("text")
			.attr("x", function(d) { return d.x; })
			.attr("y", function(d) { return d.y; });

		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
	}
	});
});

function node_click(d) {
	d3.select(this).attr("class", 
		function() {  
			if (d3.select(this).attr("class") == "selected") {
				delNodeUserDiv(d.id);
				return "";
			} else {
				addNodeUserDiv(d.id, d.name);
				return "selected";
			}
		});
//	alert(d.name);
}

function addNodeUserDiv(nodeID, nodeName) {
	$('#nodeLogins').html($('#nodeLogins').html() + "<form class='logform' id='" + nodeID +"'>"
+nodeName +"<br>UserName:<br><input type='text' name='username'><br>Password:<br><input type='password' name='password'></form>");
}

function delNodeUserDiv(nodeID) {
	$('form[id="'+ nodeID+'"]').remove();
}

$('#submit').on('click', function() {
	var dataObject = {};
	dataObject.options = {};
	dataObject.systems = {};
	$('.logform').each(function() {
		var myID = $(this)[0].id;
		dataObject.systems[myID] = {};
		$( 'form[id="'+ myID +'"] :input').each(function() {
			dataObject.systems[myID][$(this)[0].name] = $(this)[0].value;
		});
	});
	$('#options :input').each(function() {
		var v = $(this)[0].value;
		if ($(this)[0].name == 'secure_enable') {
			v = $(this)[0].checked ? 1: 0;
		}
		dataObject.options[$(this)[0].name] = v;
	});
	console.log(dataObject);
	$.post("/configure", {options: JSON.stringify(dataObject.options), 
		systems: JSON.stringify(dataObject.systems)});
});

$('#os_check').on('click', function() {
	$('#os_input').prop('disabled', function(i, v) { return !v; });
});

});
