/**
 * expression.js - Expression include file that contains functions used
 * by main.js to evaluate expressions on devices.
 */
function evaluate_expression(session, scriptEnv, exp)
{
    var retval = false;

    if (!session.target.isConnected()) {
        session.target.connect();
    }

    //  Evaluate Expression
    retval = session.expression.evaluate(exp);
    //retval = session.expression.evaluateToString(exp);

    return retval;
}
