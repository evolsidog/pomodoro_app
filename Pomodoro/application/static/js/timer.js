// Timer from https://codepen.io/rajdgreat007/pen/ZpZWbw
var pomodoro = {
    started : false,
    minutes : 0,
    seconds : 0,
    fillerHeight : 0,
    fillerIncrement : 0,
    interval : null,
    minutesDom : null,
    secondsDom : null,
    fillerDom : null,
    init : function(){
      var self = this;
      this.minutesDom = document.querySelector('#minutes');
      this.secondsDom = document.querySelector('#seconds');
      this.fillerDom = document.querySelector('#filler');
      this.interval = setInterval(function(){
        self.intervalCallback.apply(self);
      }, 1000);
      document.querySelector('#work').onclick = function(){
//          var table = $('#todoTable').DataTable();
//          if (! table.rows( '.active' ).any() ){
//                alert('Please select some task in TO DO Task');
//            }
//          else{
//            var id = $.map(table.rows('.active').data(), function (item) {
//                return item[0] // Get id field
//            });
//
//            self.startWork.apply(self);
//          }
            if ($("#current_task").text() === ""){
                alert('Please select some task in TO DO Task');
            }
            else{
                self.startWork.apply(self);
            }

      };
      document.querySelector('#shortBreak').onclick = function(){
        self.startShortBreak.apply(self);
      };
      document.querySelector('#longBreak').onclick = function(){
        self.startLongBreak.apply(self);
      };
      document.querySelector('#stop').onclick = function(){
        self.stopTimer.apply(self);
      };
      document.querySelector('#done').onclick = function(){
          idCurrentTask = $("#id_current_task").val()
          if (idCurrentTask != "") {
              $.ajax({
                  type: "POST",
                  contentType: "application/json; charset=utf-8",
                  url: "/end_task",
                  data: JSON.stringify({"id_current_task": idCurrentTask}),
                  success: function () {
                    console.log("task finished");
                  },
                  dataType: "json"
                });
          }
      }
    },
    resetVariables : function(mins, secs, started){
      this.minutes = mins;
      this.seconds = secs;
      this.started = started;
      this.fillerIncrement = 200/(this.minutes*60);
      this.fillerHeight = 0;
    },
    startWork: function() {
      this.resetVariables(0, 10, true);
    },
    startShortBreak : function(){
      this.resetVariables(5, 0, true);
    },
    startLongBreak : function(){
      this.resetVariables(15, 0, true);
    },
    stopTimer : function(){
      this.resetVariables(25, 0, false);
      this.updateDom();
    },
    toDoubleDigit : function(num){
      if(num < 10) {
        return "0" + parseInt(num, 10);
      }
      return num;
    },
    updateDom : function(){
      this.minutesDom.innerHTML = this.toDoubleDigit(this.minutes);
      this.secondsDom.innerHTML = this.toDoubleDigit(this.seconds);
      this.fillerHeight = this.fillerHeight + this.fillerIncrement;
      this.fillerDom.style.height = this.fillerHeight + 'px';
    },
    intervalCallback : function(){
      if(!this.started) return false;
      if(this.seconds == 0) {
        if(this.minutes == 0) {
          this.timerComplete();
          return;
        }
        this.seconds = 59;
        this.minutes--;
      } else {
        this.seconds--;
      }
      this.updateDom();
    },
    playAudio: function(){
      var x = document.getElementById("alarm_sound");
      x.play();
    },
    timerComplete : function(){
      this.started = false;
      this.fillerHeight = 0;
      this.playAudio();
      // Add pomodoro in DB
      idCurrentTask = $("#id_current_task").val()
      $.ajax({
          type: "POST",
          contentType: "application/json; charset=utf-8",
          url: "/add_pomodoro",
          data: JSON.stringify({"id_current_task": idCurrentTask}),
          success: function (data) {
            $("#current_pomodoros").text(data.current_task_pomodoros.toString());
          },
          dataType: "json"
        });
    }
};
window.onload = function(){
  pomodoro.init();
};

// TO DO Datatable
$(document).ready(function() {
    var table = $('#todoTable').DataTable( {
    // Hide first column with user id
        "columns": [
            { "visible": false },
            null,
            null,
        ] } );

    $('#todoTable tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('active') ) {
            $(this).removeClass('active');
            $("#current_task").text("");
            $("#current_pomodoros").text("");
            $("#id_current_task").val("");
        }
        else {
            table.$('tr.active').removeClass('active');
            $(this).addClass('active');
            var row = $.map(table.rows('.active').data(), function (item) {
                return item // Get id field
            });
            id = row[0]
            name = row[2]
            $("#current_task").text(name);
            if ($("#current_pomodoros").text() == ""){
                $("#current_pomodoros").text(0);
            }
            $("#id_current_task").val(id);
        }
    } );

} );

// DONE Datatable
$(document).ready(function() {
    var table = $('#pastTable').DataTable();
    $('#pastTable tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('active') ) {
            $(this).removeClass('active');
        }
        else {
            table.$('tr.active').removeClass('active');
            $(this).addClass('active');
        }
    } );

} );
