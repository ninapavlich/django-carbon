try {
    $(document).ready(function() {    
        /* CHOSEN ELEMENTS */    
        var selects = $("select");
        $(selects).each(function(index, item) {
            //if has class no-chosen, don't do a chosen
            if($(item).hasClass( 'no-chosen' )){
                //console.log("skip chosen.")

            }else{
                var isImage = $(item).hasClass( 'image' );
                var doChosen = $(item).hasClass( 'do-chosen' );
                var attr = $(item).attr('multiple');
                var isMultiple = (typeof attr !== typeof undefined && attr !== false);
                var hasEnoughItems = $(item).find('option').size() > 15;
                var isTouch = $(".touch").length >= 1;
                
                var isSomeSortOfChosen = (isImage || doChosen || isMultiple || hasEnoughItems) && (isTouch==false);
                
                //console.log("doChosen? "+doChosen+" isMultiple? "+isMultiple+" hasEnoughItems? "+hasEnoughItems+" isTouch? "+isTouch);
                /* Clear out first placeholder item for better rendering */
                if(isSomeSortOfChosen){
                    var options = $(item).find("option");
                    if(options.length > 0){
                        var firstOption = options[0];
                        var firstValue = $(firstOption).attr("value");
                        var isEmpty = typeof(firstValue)=='undefined' || firstValue == '';
                        if(isEmpty){
                            $(firstOption).text('')
                        }                    
                    }

                    
                    try {}catch(e) { Raven.captureException(e);}
                    if(isImage){
                        $(item).imageChosen({});    
                    }else if(doChosen || isMultiple || hasEnoughItems){
                        $(item).chosen({}); 
                    } 
                  
                }

                

                $(item).bind("change", function(event){
                    selectValueChanged(this);
                })
            }

            function selectValueChanged(item){
                if($(item).val()==''){
                    $(item).removeClass("hasValue");
                }else{
                    $(item).addClass("hasValue");
                }
            }
            
            selectValueChanged(item);

        });
    });

}catch(e) { console.log("Error in carbon_forms.js")} 