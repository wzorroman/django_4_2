$(document).ready(function() {
    $("input").keydown(function (e){
       let keyCode = e.which;
       if (keyCode == 13){
         e.preventDefault();
         return false;
       }
    });

    $("form").on("submit", function () {
        $(this).find("select, input").prop("disabled", false);
        $(this).find("button[type='submit']").prop("disabled",true).html("Procesando");
        toastr.info("Procesando, favor de esperar...");
        return true;
    });

})

// add style when focus on input text
$("input:text, select, input[type='number'], input[type='date']").bind("focus blur", function() {
    $(this).toggleClass("light_yellow");
});

$("textarea").bind("focus blur", function() {
    $(this).toggleClass("light_yellow");
});


function disabledFields(listIdFields) {
    listIdFields.forEach(function (idElement){
        $(idElement).prop("disabled", true);
    })
}

function enabledFields(listIdFields) {
    listIdFields.forEach(function (idElement){
        $(idElement).prop("disabled", false);
    })
}

function addReadOnlyFields(listIdFields) {
    listIdFields.forEach(function (idElement){
        $(idElement).attr('readonly',true);
    })
}

function removeReadOnlyFields(listIdFields) {
    listIdFields.forEach(function (idElement){
        $(idElement).removeAttr("readonly")
    })
}

function disabledRequired(listIdFields) {
    listIdFields.forEach(function (idElement){
        $(idElement).removeAttr('required');
    })
}

function enabledRequired(listIdFields) {
    listIdFields.forEach(function (idElement){
        $(idElement).attr('required', 'required');
    })
}

function addClassToFields(listIdFields, setClass) {
    listIdFields.forEach(function (idElement){
        $(idElement).addClass(setClass);
    })
}

function removeClassToFields(listIdFields, setClass) {
    listIdFields.forEach(function (idElement){
        $(idElement).removeClass(setClass);
    })
}

function restartCboToFirstElement(listIdFields, setClass) {
    listIdFields.forEach(function (idElement){
        $(idElement).prop("selectedIndex", 0);
    })
}
function clearContentFromInput(listIdFields, setClass) {
    listIdFields.forEach(function (idElement){
        $(idElement).val("");
    })
}
