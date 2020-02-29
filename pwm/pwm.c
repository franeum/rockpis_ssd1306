#include "m_pd.h"  
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>

/* mraa header */
#include "mraa/pwm.h"

/* gpio declaration */
// #define GPIO_PIN_1 22

/* PWM declaration */
#define PWM 3

/* PWM period in us */
#define PWM_FREQ 200

static t_class *pwm_class;  
 
typedef struct _pwm {  
  	t_object x_obj;
	volatile sig_atomic_t flag;
	int state;
 	mraa_result_t status;
    	//mraa_gpio_context gpio_1;
	mraa_pwm_context pwm;
} t_pwm;  



/* gestisce l'uscita */

void sig_handler(t_pwm *x, int signum)
{
    if (signum == SIGINT) {
        fprintf(stdout, "Exiting...\n");
        x->flag = 0;
    }
}

void pwm_free(t_pwm *x)
{

    /* release gpio's */
    x->status = mraa_pwm_close(x->pwm);

    //! [Interesting]
    /* deinitialize mraa for the platform (not needed most of the times) */
    mraa_deinit();
}

void pwm_float(t_pwm *x, t_floatarg f)  
{
  //(void)x; // silence unused variable warning
  //x->state = 1 - x->state;
  post("%d", f);
  x->status = mraa_pwm_write(x->pwm, f);
}

void *pwm_new(void)  
{  
  t_pwm *x = (t_pwm *)pd_new(pwm_class);  
  x->flag = 1;
  x->state = 0;

    x->status = MRAA_SUCCESS;

    	/* install signal handler */
    	//signal(SIGINT, sig_handler);

    /* initialize mraa for the platform (not needed most of the times) */
    mraa_init();
    x->pwm = mraa_pwm_init(PWM);
    //! [Interesting]
    /* initialize GPIO pin */
    //x->gpio_1 = mraa_gpio_init(GPIO_PIN_1);
    x->status = mraa_pwm_period_us(x->pwm, PWM_FREQ);
    
    x->status = mraa_pwm_enable(x->pwm, 1);
    
    
    /* set GPIO to output */
    //x->status = mraa_gpio_dir(x->gpio_1, MRAA_GPIO_OUT);
    

  return (void *)x;  
}  
 
void pwm_setup(void) {  
  pwm_class = class_new(gensym("pwm"),  
    (t_newmethod)pwm_new, NULL,
    sizeof(t_pwm), CLASS_DEFAULT, 0);  
  class_addfloat(pwm_class, pwm_float);  
}
