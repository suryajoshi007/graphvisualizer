$(document).ready(function(){
	$myimage=$("#myimage");
	d=new Date();
	$("#myerrordiv").hide();
	$("#mysuccessdiv").hide();
	
	$("#mysubmit").on("click",function(event) {
			$.ajax({
			
			type:"POST",
			data:JSON.stringify({
				"select":$("#myselect").val(),
				"codes":$("#mycodes").val(),
			}),
			url:"/echo2",
			contentType: 'application/json;charset=UTF-8',
			success: function(data){
				if(data.error)
				{
					$("#myimage").hide();
					$("#mysuccessdiv").hide();
					$("#myerror").text(data.error);
					$("#myerrordiv").show();
				}
				else
				{
					$("#myerrordiv").hide();
					$("#mysuccess").text("graph successfully built!!");
					$("#mysuccessdiv").show()
					$myimage.attr("src", "/static/g.png?"+Math.random());
					$myimage.show();

				}
			},
			error: function(){

			},
		});
		event.preventDefault();
	});
});