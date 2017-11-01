/**
 * Created with PyCharm.
 * User: stone
 * Date: 12-12-10
 * Time: 下午3:06
 * To change this template use File | Settings | File Templates.
 */
function changevalCityIns(targetObj,parentid,selectedid)
{
    var newoptsarr=new Array();
    var newoptsarrval=new Array();
    var newoptionI=0;
    //清除现有
    count1=targetObj.options.length;
    while(count1!=0)
    {
        targetObj.options.remove(0);
        count1=targetObj.options.length;
    }
    //过滤上级id=选中id
    for(var i=0;i<arrayCity.length;i++)
    {
        if(arrayCity[i][2]==parentid)
        {
            newoptsarr[newoptionI]=arrayCity[i][0];
            newoptsarrval[newoptionI]=arrayCity[i][3];
            var aOption = new Option(arrayCity[i][3],arrayCity[i][0]);
            targetObj.options[newoptionI]=aOption;
            if(arrayCity[i][0]==selectedid)
            {
                targetObj.options[newoptionI].selected=true;
            }
            newoptionI++;
        }
    }
    if(targetObj.id=="sheng")
    {
        changevalCityIns(document.getElementById("shi"),newoptsarr[0],0)
    }
    if(targetObj.id=="shi")
    {
        changevalCityIns(document.getElementById("xian"),newoptsarr[0],0)
    }
}

function changevalCityPls(targetObj,parentid,selectedid)
{
    var newoptsarr=new Array();
    var newoptsarrval=new Array();
    var newoptionI=0;
    //清除现有
    count1=targetObj.options.length;
    while(count1!=0)
    {
        targetObj.options.remove(0);
        count1=targetObj.options.length;
    }
    //过滤上级id=选中id
    for(var i=0;i<arrayCity.length;i++)
    {
        if(arrayCity[i][2]==parentid)
        {
            newoptsarr[newoptionI]=arrayCity[i][0];
            newoptsarrval[newoptionI]=arrayCity[i][3];
            var aOption = new Option(arrayCity[i][3],arrayCity[i][0]);
            targetObj.options[newoptionI]=aOption;
            if(arrayCity[i][0]==selectedid)
            {
                targetObj.options[newoptionI].selected=true;
            }
            newoptionI++;
        }
    }
    if(targetObj.id=="idINSURANT_USR_sheng")
    {
        changevalCityPls(document.getElementById("idINSURANT_USR_shi"),newoptsarr[0],0)
    }
    if(targetObj.id=="idINSURANT_USR_shi")
    {
        changevalCityPls(document.getElementById("idINSURANT_USR_xian"),newoptsarr[0],0)
    }
}

function changevalCityPlsA(targetObj,parentid,selectedid)
{
    var newoptsarr=new Array();
    var newoptsarrval=new Array();
    var newoptionI=0;
    //清除现有
    count1=targetObj.options.length;
    while(count1!=0)
    {
        targetObj.options.remove(0);
        count1=targetObj.options.length;
    }
    //过滤上级id=选中id
    for(var i=0;i<arrayCity.length;i++)
    {
        if(arrayCity[i][2]==parentid)
        {
            newoptsarr[newoptionI]=arrayCity[i][0];
            newoptsarrval[newoptionI]=arrayCity[i][3];
            var aOption = new Option(arrayCity[i][3],arrayCity[i][0]);
            targetObj.options[newoptionI]=aOption;
            if(arrayCity[i][0]==selectedid)
            {
                targetObj.options[newoptionI].selected=true;
            }
            newoptionI++;
        }
    }
    if(targetObj.id=="idINSURANT_USR_shengA")
    {
        changevalCityPlsA(document.getElementById("idINSURANT_USR_shiA"),newoptsarr[0],0)
    }
    if(targetObj.id=="idINSURANT_USR_shiA")
    {
        changevalCityPlsA(document.getElementById("idINSURANT_USR_xianA"),newoptsarr[0],0)
    }
}

function changevalCityPlsB(targetObj,parentid,selectedid)
{
    var newoptsarr=new Array();
    var newoptsarrval=new Array();
    var newoptionI=0;
    //清除现有
    count1=targetObj.options.length;
    while(count1!=0)
    {
        targetObj.options.remove(0);
        count1=targetObj.options.length;
    }
    //过滤上级id=选中id
    for(var i=0;i<arrayCity.length;i++)
    {
        if(arrayCity[i][2]==parentid)
        {
            newoptsarr[newoptionI]=arrayCity[i][0];
            newoptsarrval[newoptionI]=arrayCity[i][3];
            var aOption = new Option(arrayCity[i][3],arrayCity[i][0]);
            targetObj.options[newoptionI]=aOption;
            if(arrayCity[i][0]==selectedid)
            {
                targetObj.options[newoptionI].selected=true;
            }
            newoptionI++;
        }
    }
    if(targetObj.id=="idINSURANT_USR_shengB")
    {
        changevalCityPlsB(document.getElementById("idINSURANT_USR_shiB"),newoptsarr[0],0)
    }
    if(targetObj.id=="idINSURANT_USR_shiB")
    {
        changevalCityPlsB(document.getElementById("idINSURANT_USR_xianB"),newoptsarr[0],0)
    }
}

function changevalCityPlsC(targetObj,parentid,selectedid)
{
    var newoptsarr=new Array();
    var newoptsarrval=new Array();
    var newoptionI=0;
    //清除现有
    count1=targetObj.options.length;
    while(count1!=0)
    {
        targetObj.options.remove(0);
        count1=targetObj.options.length;
    }
    //过滤上级id=选中id
    for(var i=0;i<arrayCity.length;i++)
    {
        if(arrayCity[i][2]==parentid)
        {
            newoptsarr[newoptionI]=arrayCity[i][0];
            newoptsarrval[newoptionI]=arrayCity[i][3];
            var aOption = new Option(arrayCity[i][3],arrayCity[i][0]);
            targetObj.options[newoptionI]=aOption;
            if(arrayCity[i][0]==selectedid)
            {
                targetObj.options[newoptionI].selected=true;
            }
            newoptionI++;
        }
    }
    if(targetObj.id=="idINSURANT_USR_shengC")
    {
        changevalCityPlsC(document.getElementById("idINSURANT_USR_shiC"),newoptsarr[0],0)
    }
    if(targetObj.id=="idINSURANT_USR_shiC")
    {
        changevalCityPlsC(document.getElementById("idINSURANT_USR_xianC"),newoptsarr[0],0)
    }
}

function changevalCityDel(targetObj,parentid,selectedid)
{
    var newoptsarr=new Array();
    var newoptsarrval=new Array();
    var newoptionI=0;
    //清除现有
    count1=targetObj.options.length;
    while(count1!=0)
    {
        targetObj.options.remove(0);
        count1=targetObj.options.length;
    }
    //过滤上级id=选中id
    for(var i=0;i<arrayCity.length;i++)
    {
        if(arrayCity[i][2]==parentid)
        {
            newoptsarr[newoptionI]=arrayCity[i][0];
            newoptsarrval[newoptionI]=arrayCity[i][3];
            var aOption = new Option(arrayCity[i][3],arrayCity[i][0]);
            targetObj.options[newoptionI]=aOption;
            if(arrayCity[i][0]==selectedid)
            {
                targetObj.options[newoptionI].selected=true;
            }
            newoptionI++;
        }
    }
    if(targetObj.id=="shengDel")
    {
        changevalCityDel(document.getElementById("shiDel"),newoptsarr[0],0)
    }
    if(targetObj.id=="shiDel")
    {
        changevalCityDel(document.getElementById("xianDel"),newoptsarr[0],0)
    }
}

function changevalGrpUsrIns(targetObj,parentid,selectedid)
{
    //alert("haha");

    //alert("parentid is : "+parentid);
    //alert("selectedid is : "+selectedid);

    var newoptsarr=new Array();
    var newoptsarrval=new Array();
    var newoptionI=0;
    //清除现有
    count1=targetObj.options.length;
    while(count1!=0)
    {
        targetObj.options.remove(0);
        count1=targetObj.options.length;
    }
    //过滤上级id=选中id
    for(var i=0;i<arrayGrpUsr.length;i++)
    {
        if(arrayGrpUsr[i][2]==parentid)
        {
            newoptsarr[newoptionI]=arrayGrpUsr[i][0];
            newoptsarrval[newoptionI]=arrayGrpUsr[i][3];
            var aOption = new Option(arrayGrpUsr[i][3],arrayGrpUsr[i][0]);
            targetObj.options[newoptionI]=aOption;
            if(arrayGrpUsr[i][0]==selectedid)
            {
                targetObj.options[newoptionI].selected=true;
            }
            newoptionI++;
        }
    }

    //alert("parentid is : "+parentid);
    //alert("selectedid is : "+selectedid);

    if(targetObj.id=="idGrpValue")
    {
        //alert ("in idGrpValue");
        changevalGrpUsrIns(document.getElementById("idUsrValue"),newoptsarr[0],0);
    }
    if(targetObj.id=="idUsrValue")
    {
        //changevalGrpUsrIns(document.getElementById("xian"),newoptsarr[0],0):
    }
}


