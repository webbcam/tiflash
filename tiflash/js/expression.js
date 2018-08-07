/**
 * expression.js - Expression include file that contains functions used
 * by main.js to evaluate expressions on devices.
 */
function evaluate_expression(session, scriptEnv, eval)
{
    var retval = false;

    if (!session.target.isConnected()) {
        session.target.connect();
    }

    //  Load Symbols
    if (eval.symbols) {
        session.symbol.load(eval.symbols);
    }

    //  Evaluate Expression
    retval = session.expression.evaluate(eval.expression);

    return retval;
}
