from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource, abort

app = Flask(__name__)
api = Api(app)

transactions = {}

class Balance(Resource):
    def get(self):
        res = {}
        for payer, amount in transactions.values():
            if payer in res:
                res[payer] += amount
            else:
                res[payer] = amount
        return make_response(jsonify(res), 200)
    
class Add(Resource):
    def post(self):
        if not request.is_json:
            abort(400, message="request must be in JSON format (ensure Content-Type is set to 'application/json')")
        data = request.get_json(force=True)
        for field in ['payer', 'points', 'timestamp']:
            if field not in data:
                abort(400, message=f"missing field '{field}'")
        payer = data['payer']
        points = data['points']
        timestamp = data['timestamp']
        if timestamp in transactions:
            abort(400, message="There is already a transaction at the given time")
        transactions[timestamp] = [payer, points]
        return make_response('', 200)
    
class Spend(Resource):
    def post(self):
        if not request.is_json:
            abort(400, message="request must be in JSON format (ensure Content-Type is set to 'application/json')")
        data = request.get_json(force=True)
        if "points" not in data:
            abort(400, message=f"missing field 'points'")
        points = data['points']
        tot = 0
        for _, val in transactions.values():
            tot += val
        if tot < points:
            return make_response("user doesn't have enough points", 400)
        curr = {}
        for payer, amount in transactions.values():
            if payer in curr:
                curr[payer] += amount
            else:
                curr[payer] = amount
        res = []
        indicies = {}
        for time in sorted(transactions.keys()):
            if points <= 0:
                break
            payer, amount = transactions[time]
            diff = amount if points > amount else points
            if curr[payer] - diff < 0:
                continue
            curr[payer] -= diff
            points -= diff
            transactions[time][1] -= diff
            if payer in indicies:
                res[indicies[payer]]["points"] -= diff
            else:
                indicies[payer] = len(res)
                res.append({"payer": payer, "points": -diff})
        return make_response(jsonify(res), 200)

    
api.add_resource(Balance, '/balance')
api.add_resource(Add, '/add')
api.add_resource(Spend, '/spend')

if __name__ == '__main__':
    app.run(debug=True, port=8000)