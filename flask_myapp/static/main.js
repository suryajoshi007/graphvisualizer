function myfunction()
{
	document.getElementById("demo").innerHTML="paragraph changed"
}

simon=document.getElementById("btnsimon")
bruce=document.getElementById("btnbruce")
ben=document.getElementById("btnben")

simon.addEventListener("focus",piclink)
bruce.addEventListener("focus",piclink)
ben.addEventListener("focus",piclink)
 
function piclink()
{
	var images=document.getElementsByTagName("img");
	for(var i=0;i<images.length;i++)
	{
		images[i].className="hide";
	}
	var picid=this.attributes["data-img"].value;
	var pic=document.getElementById(picid);

	if(pic.className === "hide")
	{
		pic.className = "";
	}
	else
	{
		pic.className = "hide";
	}
}

var checklist=document.getElementById("checklist");
var items=checklist.getElementsByTagName("li");
var inputs=checklist.getElementsByTagName("input");

for(var i=0;i<items.length;i++)
{
	console.log(items[i]);
	items[i].addEventListener("click",editlist);
	inputs[i].addEventListener("mouseleave",inputlist);
	inputs[i].addEventListener("keypress",keylist);


}


function editlist()
{
	this.className="edit";
}

function inputlist()
{
	console.log("we blured");
	this.previousElementSibling.innerHTML=this.value;
	this.parentNode.className="";
}

function keylist()
{
	if(event.which===13)
	{
		inputlist.call(this);
	}
}



















