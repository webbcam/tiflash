/**
 * expression.js - Expression include file that contains functions used
 * by main.js to evaluate expressions on devices.
 */
function evaluate_expression(session, scriptEnv, expr)
{
    var retval = false;

    if (!session.target.isConnected()) {
        session.target.connect();
    }

    //  Evaluate Expression
    retval = session.expression.evaluate(expr.expr);
    //retval = session.expression.evaluateToString(expr.expr);

    return retval;
}
