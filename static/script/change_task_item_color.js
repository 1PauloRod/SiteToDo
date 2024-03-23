
document.addEventListener('DOMContentLoaded', function () {
    var task_itens = document.querySelectorAll('.task-item');
  
    task_itens.forEach(function(item){
        item.addEventListener('click', function(){
            this.classList.toggle('clicked');
        });
    });
  });